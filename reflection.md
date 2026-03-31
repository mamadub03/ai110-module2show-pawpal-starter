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

- I used Copilot to review class designs (Owner, Pet, Task, Constraints, Schedule, Scheduler), write concise method logic, and debug behavior with read_file + test-driven updates.
- Most helpful prompts were defect reports like "utf-8 codec can't decode" and "update UML diagram based on final implementation".

**b. Judgment and verification**

- Copilot suggested using raw glyphs `"���"` in `app.py` for emojis; I rejected that and replaced with valid UTF-8 `"🐾"` and an explicit encoding header.
- I verified by reading the file content and running the app in Streamlit after a code fix.

**c. Specific Copilot features**

- Context-aware code completion (suggesting methods and class fields).
- Quick code scanning and system-level architecture explanation from existing module content.
- Assisted in structured README/reflection updates.

**d. Separate chat sessions benefit**

- Breaking design, code fix, and reflection into separate prompts kept focus and reduced confusion.
- I could lock in working logic before writing the final reflective narrative.

---

## 4. Testing and Verification

**a. What you tested**

- Verified `Task.mark_done()` sets `done=True` and creates a new recurring task when `recurrence` is `daily` or `weekly`.
- Verified `Owner.filter_tasks(done, pet_name)` selects correct tasks by status and pet.
- Verified `Scheduler.prioritize()` orders incomplete required high-priority short tasks first.
- Verified `Scheduler.detect_conflicts()` returns warnings for overlapping entries when explicit start/end times exist.

These tests are important because they guard core scheduling behavior and prevent regressions when adjusting task or plan logic.

**b. Confidence**

- I am fairly confident (~4/5) that the scheduler handles typical use cases correctly. The logic is straightforward and covered by targeted tests, but complex savings (calendar scheduling, buffer times, multi-day planning) are not yet implemented.
- If I had more time, I would add tests for: overlapping tasks with unsorted start times, block-period-aware constraint filtering, `max_tasks` boundary conditions, and owner preference-based filtering.

---

## 5. Reflection

**a. What went well**

- I’m most satisfied that the implementation supported the full workflow from owner/pet/task modeling to schedule generation and explanation with conflict detection.
- The system is modular: data objects are separated from scheduling strategies, which makes testing and extension easier.

**b. What you would improve**

- Next iteration would add explicit `Task` time windows, better conflict resolution (not just detection), and a UI workflow for editing/removing tasks in the schedule.
- I would also implement persistence (save/load owner state) and multi-owner support clearly in the UI.

**c. Key takeaway**

- Leading architecture with AI support means setting clear structure and accepting suggestions carefully, not automatically. AI is strongest as a collaborator for small refactors and code patterns, while the lead architect ensures correctness, simplicity, and alignment with requirements.
