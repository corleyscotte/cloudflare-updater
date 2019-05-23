# cloudflare-updater
Update cloudflare records with your dynamic public IP


GET STARTED:

Step 1:
Go to https://dash.cloudflare.com/profile
Scroll down to "Global API Key" and select 'View'
Enter your CloudFlare password in the prompt
Copy your CloudFlare Global API Key
Replace CLOUDFLARE_API_KEY value with your copied key

Step 2:
Go to https://www.cloudflare.com/a/overview/
Click on domain you want to update
Scroll down to lower right side and copy "Zone ID" value
Replace CLOUDFLARE_ZONE_ID value with your zone ID

Step 3:
Replace CLOUDFLARE_EMAIL value with your registered CloudFlare email
Replace SUBDOMAINS_TO_UPDATE with any subdomains you want to update
Replace DOMAIN with your domain name (example.com)

Step 4:
Ensure DNS records exist prior to running this updater script
Run this script ./cloudflare-updater.property

HOW TO SCHEDULE:

TODO: Crontab instructions coming soon...

