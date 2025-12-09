echo "Enter your email address for alert notifications:"
read EMAIL

echo "Please input your DigitalOcean API Token:"
read DIGITALOCEAN_TOKEN

droplets=$(curl -X GET \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/droplets" | jq '.droplets')

echo "$droplets" | jq -c '.[]' | while read item; do
    # Extract image name and check if it contains 'kube'
    image_name=$(echo "$item" | jq -r '.image.name')
    
    if [[ "$image_name" == *"kube"* ]]; then
        echo "Found 'kube' in image.name: $image_name"
        droplet_id=$(echo "$item" | jq -r '.id')
        droplet_name=$(echo "$item" | jq -r '.name')
        echo "Droplet ID: $droplet_id for Droplet $droplet_name"

        # Create CPU alert for the droplet
        curl -X POST \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
          "https://api.digitalocean.com/v2/monitoring/alerts" \
          --data '{
              "alerts":{
                "email":["'$EMAIL'"]
              },
              "compare":"GreaterThan",
              "description":"CPU Alert for droplet $droplet_name",
              "enabled":true,
              "entities":["'$droplet_id'"],
              "tags":["droplet_tag"],
              "type":"v1/insights/droplet/cpu",
              "value":80,
              "window":"5m"
            }'

        # Create Disk Utilization alert for the droplet
        curl -X POST \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
          "https://api.digitalocean.com/v2/monitoring/alerts" \
          --data '{
              "alerts":{
                "email":["'$EMAIL'"]
              },
              "compare":"GreaterThan",
              "description":"Disk Utilization Alert for droplet $droplet_name",
              "enabled":true,
              "entities":["'$droplet_id'"],
              "tags":["droplet_tag"],
              "type":"v1/insights/droplet/disk_utilization_percent",
              "value":80,
              "window":"5m"
            }'
        # Create Memory alert for the droplet
        curl -X POST \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
          "https://api.digitalocean.com/v2/monitoring/alerts" \
          --data '{
              "alerts":{
                "email":["'$EMAIL'"]
              },
              "compare":"GreaterThan",
              "description":"Memory Alert for droplet $droplet_name",
              "enabled":true,
              "entities":["'$droplet_id'"],
              "tags":["droplet_tag"],
              "type":"v1/insights/droplet/memory_utilization_percent",
              "value":80,
              "window":"5m"
            }'
          

    fi
done