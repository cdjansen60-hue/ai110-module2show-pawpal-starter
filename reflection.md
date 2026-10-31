# PawPal+ Project Reflection

## 1. System Design

**Three Core Actions**
- Add a pet
- Schedule a task (Task can be broken down into walks, feeding, med, grooming, etc.)
- See today's tasks

**a. Initial design**

My initial design was just Tasks, Pets, and the Schedular. The schedular held the scheduled tasks and the Task objects were time agnostic, with the assumption that the schedular would handle multiple instances of a task object for a different scheduled time/date.

**b. Design changes**

Claude pointed out that later in the assignment that it expects a certain object structure - notably an Owner object (in hindsight, I should have considered this first, I was expecting only one owner per app initially). This changed the hierarchy considerably so that the Schedular no longer owns any data, and instead points to the data held by Owners, Pets, and Tasks respectively.

Upon review of the skeleton by Claude, I chose to update the task relationship to include a reference to the pet it was for. Time strings were updated to be datetime.time objects for validation and ease of sorting. Priority and Frequency were updated to be enum values instead of free strings. A method to get a pet by name through the Owner was also added for future sorting. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler only handles exact start-time conflicts. This may result in overlapping tasks, but that is a decision for the owner to make (i.e. in the case of an overlapping recurring task). Overlapping tasks are not always necessarily an issue.
---

## 3. AI Collaboration

**a. How you used AI**

I used Claude for this project for most things. Initial development was slow as the design came together, but eventually it was mostly Claude debugging/refactoring after approval for design changes. The most helpful prompts were the ones that established the rules of the project. (i.e. "I am the architect, don't make decisions on your own")

**b. Judgment and verification**

At the very beginning Claude immediately tried to build the entire project. I had to walk it back so I would act as the architect. Beyond that, I had some design decisions I chose based on this exercise rather than some of Claude's more extensive suggestions. For example, one design decision was to have the tasks hold a reference to pets, even though that could introduce recursion. I chose this for code simplicity, rather than re-architecting the structure. My general opinion is these exercises should follow a minimal viable product(MVP) approach.

---

## 4. Testing and Verification

**a. What you tested**

Tests covered basic functionality, sorting, recurrence, conflict detection, filtering, edge cases, and data integrity. These are important to both prove functionality and maintain future code changes.

**b. Confidence**

I am reasonably confident the scheduler works in most cases. Edge cases I would test are duration overlap, late recurring task completion, UI tests, and code that intentionally breaks the pets/tasks recursion issue mentioned above.

---

## 5. Reflection

**a. What went well**

I'm pretty happy with how quickly the problem collapsed upon itself once the design was created.

**b. What you would improve**

Maybe a re-look at the object member heirarchy to avoid the recursion issue.

**c. Key takeaway**

AI is very good at taking a finalized concept and implementing it. This extends to edge-cases it finds along the way. That being said, if the initial concept isn't fully fleshed out, the final implementation reflects that. Though that could be said for non-AI projects as well.
