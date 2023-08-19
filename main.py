import requests
import src.telegram as tele
import src.settings as settings
import src.sources.github as github
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import json

# Load previously notified versions from file, or initialize an empty dictionary if the file doesn't exist
try:
  with open('last_notified_versions.json', 'r') as f:
    last_notified_versions = json.load(f) 
except FileNotFoundError:
  last_notified_versions = {}

async def main():
    """
    Main function that checks for updates in programs and sends notifications if necessary.
    """
    programs = settings.PROGRAMS
    for program in programs:
        program_name = program['name']
        if program_name not in last_notified_versions:
            last_notified_versions[program_name] = None

        if 'github' in program:
            try:
                our_version = program['version']
                our_version = our_version.lower().replace('v', '')
                
                github_data = github.fetch_from_github(program)
                latest_version = github_data['tag_name']
                latest_version = latest_version.lower().replace('v', '')
                
                # Compare versions
                
                latest_split = latest_version.split('.')
                our_split = our_version.split('.')

                if latest_version != last_notified_versions[program_name]:
                    message = ""
                    major = False
                    minor = False
                    patch = False
                    
                    if latest_split[0] > our_split[0]:
                        message += "** 🔥 Major update **\n"
                        major = True
                    elif latest_split[1] > our_split[1]:
                        message += "** 🚀 Minor update **\n"
                        minor = True
                    elif latest_split[2] > our_split[2]:
                        message += "** 🐛 Patch update **\n"
                        patch = True
                    
                    
                    # Create notification message
                    
                    if major or minor or patch:
                        message += f"** {program['name']} ** has a new release on GitHub \n\n"
                        message += f"** {our_version} ** -> ** {latest_version} ** \n\n" 
                        message += f"[🔗 LINK]({github_data['html_url']}) \n"
                        message += f"** date: {github_data['published_at']} ** \n"
                        
                        try:
                            await asyncio.wait_for(
                              tele.send_notification(message=message), 
                              timeout=5
                             )
                            print(f"Message sent for {program['name']}")

                            last_notified_versions[program['name']] = latest_version
                            with open('last_notified_versions.json', 'w') as f:
                                json.dump(last_notified_versions, f)

                        except asyncio.TimeoutError:
                            print(f"Timeout occurred while sending message for {program['name']}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while requesting GitHub data for {program['name']}: {str(e)}")
            except KeyError as e:
                print(f"An error occurred while parsing GitHub data for {program['name']}: {str(e)}")
                
        # elif 'gitlab' in program:
        #     try:
        #         gitlab_url = f"{program['gitlab']}/api/v4/projects/{program['id']}/releases"
        #         gitlab_data = requests.get(gitlab_url).json()
        #         if gitlab_data:
        #             latest_release = datetime.strptime(gitlab_data[0]['released_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        #             if latest_release > datetime.now() - timedelta(days=1):
        #                 message = f"{program['name']} has a new release on GitLab"
        #             try:
        #                 await asyncio.wait_for(
        #                     tele.send_notification(message=message), 
        #                     timeout=5
        #                 )
        #             except asyncio.TimeoutError:
        #                 print(f"Timeout occurred while sending message for {program['name']}")
        #     except requests.exceptions.RequestException as e:
        #         print(f"An error occurred while requesting GitLab data for {program['name']}: {str(e)}")
        #     except KeyError as e:
        #         print(f"An error occurred while parsing GitLab data for {program['name']}: {str(e)}")
            
        # elif 'dockerhub' in program:
        #     try:
        #         if 'namespace' in program:
        #             dockerhub_url = f"https://hub.docker.com/v2/repositories/{program['namespace']}/{program['dockerhub']}/tags"
        #         else:
        #             dockerhub_url = f"https://hub.docker.com/v2/repositories/library/{program['dockerhub']}/tags"
        #         dockerhub_data = requests.get(dockerhub_url).json()
        #         if 'results' in dockerhub_data:
        #             latest_tag_date = max(tag['last_updated'] for tag in dockerhub_data['results'])
        #             latest_tag = datetime.strptime(latest_tag_date, '%Y-%m-%dT%H:%M:%S.%fz')
        #             if latest_tag > datetime.now() - timedelta(days=1):
        #                 message = f"{program['name']} has a new tag on Docker Hub"
        #             try:
        #                 await asyncio.wait_for(
        #                     tele.send_notification(message=message), 
        #                     timeout=5
        #                 )
        #             except asyncio.TimeoutError:
        #                 print(f"Timeout occurred while sending message for {program['name']}")
        #     except requests.exceptions.RequestException as e:
        #         print(f"An error occurred while requesting Docker Hub data for {program['name']}: {str(e)}")
        #     except KeyError as e:
        #         print(f"An error occurred while parsing Docker Hub data for {program['name']}: {str(e)}")

    

 
# Initialize scheduler
scheduler = AsyncIOScheduler()

# Add main function as a scheduled job
scheduler.add_job(
    main, 
    'interval', 
    seconds=30, 
    id='main',
    max_instances=1,  
    coalesce=True
)

# Start the scheduler
scheduler.start()

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_forever()