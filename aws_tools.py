import boto3
from datetime import datetime, timedelta, timezone


def get_idle_instances():
    """Returns running EC2 instances with their average CPU over the last 24 hours."""
    ec2 = boto3.client("ec2")
    cloudwatch = boto3.client("cloudwatch")

    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)

    results = []
    pages = ec2.get_paginator("describe_instances").paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    for page in pages:
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                stats = cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": instance["InstanceId"]}],
                    StartTime=start,
                    EndTime=end,
                    Period=3600,
                    Statistics=["Average"],
                )
                points = [p["Average"] for p in stats["Datapoints"]]
                cpu_avg = round(sum(points) / len(points), 1) if points else None
                results.append(
                    {
                        "id": instance["InstanceId"],
                        "type": instance["InstanceType"],
                        "cpu_avg": cpu_avg,
                    }
                )
    return results
