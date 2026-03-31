import requests

    def check_school(label, url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{url}/api/v1/users/self",headers = headers)
        if response.status_code == 200:
            name=response.json().get('name')
            print(f"{label} connection successful, name is: {name}")
        else:
            print(f"{label} connection failed, status:{response.status_code}")
    except Exception as e:
        print(f"{label} Error: {e}")

class CanvasProvider:
    def __init__(self, institution_name,url,token):
        self.institution_name = institution_name
        self.url = url
        self.token = token
        self.headers= {"Authorization": f"Bearer {token}"}
    
    def get_upcoming_tasks(self):
        try:
            response = requests.get(f"{self.url}/api/v1/users/self/todo", headers=self.headers)
            if response.status_code == 200:
                data=response.json()
                tasks= []
                for item in data:
                    if 'assignment' in item:
                        current_assignment_data=item['assignment']
                        task = {
                            'school': self.institution_name,
                            'course': item.get('context_name'),
                            'title': current_assignment_data.get('name'),
                            'due_at': current_assignment_data.get('due_at'),
                            'points': current_assignment_data.get('points_possible')
                        }
                        tasks.append(task)
                return tasks
            else:
                print(f"{self.institution_name} connection failed, status:{response.status_code}")
                return None
        except Exception as e:
            print(f"{self.institution_name} Error: {e}")
            return None
     