#!/bin/bash

echo "Starting deployment..."

kubectl apply -f namespace.yaml

echo "Applying secrets and configs..."
kubectl apply -f config
kubectl apply -f secrets/django-secret.yaml
echo "Are you using a Private Docker Registry? (y/N)"
read use_private_registry
if [ "$use_private_registry" == "y" ]; then
    kubectl apply -f secrets/docker-reg.yaml # Uncomment if using private Docker registry
fi
kubectl apply -f secrets/postgres-secret.yaml
kubectl apply -f secrets/do-spaces-secret.yaml

echo "Applying services, and postgres deployment..."
kubectl apply -f services
kubectl apply -f deployments/postgres-deployment.yaml

echo "Applying HPA, backup, and claim..."
kubectl apply -f hpa.yaml
kubectl apply -f claim.yaml
kubectl apply -f cronjob-backup.yaml


kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.1/deploy/static/provider/cloud/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

ip=$(kubectl -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

kubectl -n inventro create secret generic inventro-url-secret --from-literal=TRUSTED_ORIGIN="http://$ip" --from-literal=ALLOWED_HOST="$ip"

echo "Starting web deployments..."
kubectl apply -f deployments/web-deployment.yaml

kubectl wait --namespace inventro \
  --for=condition=ready pod \
  --selector=app=inventro-web \
  --timeout=120s

kubectl apply -f ingress.yaml

echo "Deployment complete. The external IP of the Ingress is $ip"
echo "To remove the deployment, run: kubectl delete namespace inventro"

