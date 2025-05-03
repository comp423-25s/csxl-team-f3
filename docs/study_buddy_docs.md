# Study Buddy Feature Implementation for CSXL Lab

## Authors

Daniel Wang: Github - https://github.com/danielwang23
Chris Zou: Github - https://github.com/chzou123
Shanyu Gowdu: Github - https://github.com/gowdu0

## Frontend

Our frontend includes two new user pages. The first page is the **Study Buddy** page. As a student, you can click on the Studdy Buddy navigation component, which will allow you to select a course from a menu that is fetched from the original CSXL's website database of classes that exist. From there, you can choose the difficulty of questions and question types you want to generate (MCQ, free response, or coding). There are 2 buttons present that allow generating either mock practice questions or a study guide.

The other page is the **Instructor Summary** page. Similarly to how the study buddy page is formatted, we have a menu to select the class the teacher would like to get a report for, then there is a button that generates a summary report of the class. The instructor page visual design is controlled thorugh the `instructor-page.component` ts and html files. Only authorized users with instructor access are able to view this page.

Also on the frontend is where we have added to the widgets of the nav bar, adding the Study Buddy under the “school section” and Instructor Summary under the "administration section." Each page is driven by its own component file (_.component.ts) and a service (_.service.ts) that handles HTTP calls.

## Backend

### Routes.py

All Studdy Buddy routing exists within our `routes.py` file under the `backend/api/study_buddy/routes.py` path.

The FastAPI router makes use of 3 Routes:

- The first route is the **GET** method, which returns a few AI-generate practice problems. This also calls the `generate_practice_problems` function, which is in the **study_buddy_service.py** file.

- Similarly, we have a **POST** method that posts a study guide of AI-generated review content. This route calls the `generate_study_guide` function in the **study_buddy_service.py** file.

- Finally, we have the **GET** method, which returns the instructor report. Similar to the other routes, this calls a service from the **study_buddy_service.py** file called `generate_instructor_report`.

Each of the services in the **study_buddy_service** file includes parameters for the ChatGPT call so that the response is properly structured and returns the correct answers. The `generate_practice_problems` and `generate_study_guide` methods use the course and course descriptions via `CourseService` and to feed the OpenAIService with the correct user and system prompts.

#### Example service method prompt

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

We reuse the class models plenty of times, but we created new models for the practice problems and study guides. All request‑and‑response shapes are defined in our `study_buddy_models.py` for PracticeProblem and StudyGuide models. These Pydantic models are then called again in our **study_buddy_service** file. We didn’t create a new model for the instructor report, but just reused our study guide response schema under the instructor report service as the guidelines were very similar.

## Database

Every time the website is loaded up, a PostgreSQL database is reloaded. This contains all of the base data that is already on the CSXL website, such as classes and other academic information. Our methods depend on the classes and refer to them in this database. We first pull the data from the database to display on our frontend for the user to select which classes they need help with. Finally, when we generate practice problems, study guides, and instructor reports, which the service layer converts the Pydantic objects into entities where our data is saved into the PostgreSQL database. We have a file called **study_buddy_entity.py**, which defines how the problems, study guides, and instructor report should be saved.

## AI Integration

The OpenAI calls are integrated into our model through the **study_buddy_service.py** file. We import the **OpenAIService** file, which was given to us, and use the method `self.openai.prompt` to call the service.

## End User Walkthrough

When a student clicks **Study Buddy** in the left navigation bar, the page shown below loads.
The panel on the left is automatically populated with every course pulled from the CSXL
catalog; selecting COMP 110 – Introduction to Programming and Data Science highlights the
course and shows its description at the top of the workspace.

![Study Buddy home screen](docs/images/study-buddy-nav.png)

After choosing a course, the student can adjust the study parameters by setting the desired
difficulty and question type. Pressing Generate Practice Problems sends those options to the backend, and the UI
displays a list of well‑formatted problems, each one with the correct answer and an explanation.

![Study Buddy Report](docs/images/study-questions.png)

For instructor users, they can click on the **Instructor Summary** widget underneath Administration → Instructor Summary. Here an instructor selects the same dynamic course list as students see and can click Generate Instructor Report to request teaching guidance for students in the class.

![Study Buddy Report](docs/images/instructor-summary-nav.png)

![Study Buddy Report](docs/images/instructor-report.png)
