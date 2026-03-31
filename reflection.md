# PawPal+ Project Reflection

## 1. System Design

- Some of the main core actions the user should be able to perform are: add/remove tasks, create a schedule based off preferences and allow for edits, new tasks for sperate pets


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Here is a brief overview of my UML design, classes, and responsibilities
Objects:
- Pet:
    Attributes = name, owner, color, height, weight
    Methods = take_walk(), give_medicine(), put_sleep(), serve_food(), groom_pet(), go_exercise()
- Task
    Attributes = name, length, preference
    Methods = remove_task, add_task, update_task, update_task_info()
- Constraints
    Attributes = time_available, prioritiy, preferences
    Methods = grabber methods
- Plan
    Attributes = plan description
    Methods = edit_plan(), explain_plan() 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    Yes I made changes to the skeletons... for example I added a new class for Owner so there could be multiple owners for different pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    One tradeoff is that the scheduler conflict check is currently written to detect overlapping task windows in a lightweight way. It is not yet doing full calendar available-slot computation (e.g., splitting tasks around partial overlaps or handling buffer times between tasks). That choice keeps the code simpler and easier to read, while still warning users when two tasks are clearly in the same time window.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
