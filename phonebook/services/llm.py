from django.urls import reverse
from openai import OpenAI
from phonebook.models import Contact
import json

class LLMPhonebookService:
    client = OpenAI()
    
    def process_prompt(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a phonebook assistant that helps users manage their contacts."},
                    {"role": "user", "content": prompt}
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "add_contact",
                            "description": "Add a new contact to the phonebook",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the contact"
                                    },
                                    "phone": {
                                        "type": "string",
                                        "description": "The phone number of the contact"
                                    }
                                },
                                "required": ["name", "phone"],
                                "additionalProperties": False
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "search_contact",
                            "description": "Search for a contact by name",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the contact to search for"
                                    }
                                },
                                "required": ["name"],
                                "additionalProperties": False
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "delete_contact",
                            "description": "Delete a contact by name",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the contact to delete"
                                    }
                                },
                                "required": ["name"],
                                "additionalProperties": False
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "update_contact",
                            "description": "Update a contact's phone number",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the contact to update"
                                    },
                                    "phone": {
                                        "type": "string",
                                        "description": "The new phone number for the contact"
                                    }
                                },
                                "required": ["name", "phone"],
                                "additionalProperties": False
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_all_contacts",
                            "description": "List all contacts in the phonebook",
                            "strict": True,
                            "parameters": {
                                "type": "object",
                                "properties": {},
                                "additionalProperties": False
                            }
                        }
                    }
                ]
            )
            
            tool_calls = completion.choices[0].message.tool_calls
            
            if len(tool_calls or '') == 1:
                name = tool_calls[0].function.name
                args = json.loads(tool_calls[0].function.arguments)
                
                return {"action": name, "args": args}
            else:
                return {"action": "unknown", "args": "Model did not execute any task."}
                
        except Exception as e:
            return {"action": "unknown", "args": f"Error parsing prompt: {str(e)}"}
        
    def process_action(self, action):
        args = action['args']
        
        try:
            match action['action']:
                case "add_contact":
                    if Contact.objects.filter(name=args['name']).exists():
                        return {
                            "url": reverse('index'),
                            "msg": f"Contact '{args['name']}' already exists."
                        }
                    
                    contact = Contact.objects.create(name=args['name'], phone=args['phone'])
                    
                    return {
                        "url": reverse('detail', args=[contact.pk]),
                        "msg": f"Added contact '{args['name']}' with phone {args['phone']}."
                    }
                
                case "search_contact":
                    contact = Contact.objects.get(name=args['name'])
                    
                    return {
                        "url": reverse('detail', args=[contact.pk]),
                        "msg": f"Found contact '{args['name']}'."
                    }
                    
                case "update_contact":
                    contact = Contact.objects.get(name=args['name'])
                    contact.phone = args['phone']
                    contact.save()
                    
                    return {
                        "url": reverse('detail', args=[contact.pk]),
                        "msg": f"Updated phone number for '{args['name']}' to {args['phone']}."
                    }
                    
                case "delete_contact":
                    contact = Contact.objects.get(name=args['name'])
                    contact.delete()
                    
                    return {
                        "url": reverse('index'),
                        "msg": f"Deleted contact '{args['name']}'."
                    }
                    
                case "list_all_contacts":
                    return {
                        "url": reverse('list'),
                        "msg": "Showing the entire phonebook."
                    }
                    
                case "unknown":
                    return {
                        "url": reverse('index'),
                        "msg": args
                    }
                    
        except Contact.DoesNotExist:
            return {
                "url": reverse('index'),
                "msg": f"No contact found with name '{args['name']}'."
            }
                        
        except Exception as e:
            return {
                "url": reverse('index'),
                "msg": f"Error processing action: {str(e)}"
            }
