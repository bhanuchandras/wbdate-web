gcloud builds submit --tag us-central1-docker.pkg.dev/data-9953189580/data-9953189580/web-country-list
gcloud run deploy web-country-list  --image us-central1-docker.pkg.dev/data-9953189580/data-9953189580/web-country-list --platform managed --region us-central1 --allow-unauthenticated
