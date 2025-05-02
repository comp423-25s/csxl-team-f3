# Study Buddy

## Frontend
Our frontend includes two new pages. The first page is the study buddy page. The study buddy page includes a menu to select the class, then dropdown menus to select the difficulty of questions/type of questions generated. Finally, there are two buttons for users to generate either practice problems or study guides.  

The other page is the instructor summary page. Similarly to how the study buddy page is formatted, we have a menu to select the class the teacher would like to get a report for, then there is a button that generates a summary report of the class.  

On the frontend, we have added to the widgets of the nav bar, adding the study buddy under the “school section” and “instructor summary” under the administration section.

## Backend

### Routes.py
Our `routes.py` file contains three routes. The first route is the **GET** method, which returns the practice problems. This also calls the `generate_practice_problems` function, which is in the **study_buddy_service.py** file.  

Similarly, we have a **POST** method that posts the study guide. This route calls the `generate_study_guide` function in the **study_buddy_service.py** file.  

Finally, we have the **GET** method, which returns the instructor report. Similar to the other routes, this calls a service from the **study_buddy_service.py** file called `generate_instructor_report`.  

Each of the services in the **study_buddy_service** file includes parameters for the ChatGPT call so that the response is properly structured and returns the correct answers.

#### Example prompt
```python
user_prompt = f"""
       Create {num_problems} practice problems for the following course:
       Course: {course_id} - {course_description}
      
       Difficulty: {difficulty if difficulty else 'Any difficulty'}
       Question Type: {question_type if question_type else 'Any type'}
      
       Each problem should:
       1. Test understanding of key concepts
       2. Be clear and unambiguous
       3. Include a detailed explanation of the correct answer
       4. Be appropriate for a computer science student
       5. Include relevant code examples if applicable
       6. If the question is listed as multiple choice, provide the correct answer and the incorrect answers.
      
       Return a JSON object with this format:
       {{
           "problems": [
               {{
               "question_text": "The question text",
               "answer": "The correct answer (if multiple choice, provide the correct answer and the incorrect answers, clearly indicated as such)",
               "explanation": "Why it's correct"
               }}
           ]
       }}
"""
```

We reuse the class models plenty of times, but we created new models for the practice problems and study guides. In our **study_buddy_models.py** file, we define both of these models. These Pydantic models are then called again in our **study_buddy_service** file. We didn’t create a new model for the instructor report, but just reused our study guide model, as the guidelines were very similar.

## Database
Every time the website is loaded up, a PostgreSQL database is reloaded. This contains all of the base data that is already on the CSXL website, such as classes and other academic information. Our methods depend on the classes and refer to them in this database. We first pull the data from the database to display on our frontend for the user to select which classes they need help with. Finally, when we generate practice problems, study guides, and instructor reports, our data is saved into the PostgreSQL database. We have a file called **study_buddy_entity.py**, which defines how the problems, study guides, and instructor reports should be saved.

## AI Integration
The OpenAI calls are integrated into our model through the **study_buddy_service.py** file. We import the **OpenAIService** file, which was given to us, and use the method `self.openai.prompt` to call the service.

