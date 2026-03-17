## Monitoring with Grafana
This repo includes a pre-built dashboard for the RKNPU.

### Auto-Import (Kubernetes)
If you use the `kube-prometheus-stack` with the dashboard sidecar enabled, simply apply the ConfigMap:
`kubectl apply -f dashboards/rknpu-configmap.yaml`

### Manual Import
1. Open Grafana.
2. Go to **Dashboards > Import**.
3. Upload the `dashboards/rknpu-dashboard.json` file.

