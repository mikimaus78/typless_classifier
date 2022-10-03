# Typless Invoice classifier

Description
---
Flask & React solution for classifying invoice documents using Typless service.

Structure
---
- fronted: react application
- backend: flask application
- database: sqlite database
- uploads: already classified pdf files
- samples: sample pdf files


Instructions
---
1. Clone repository
2. Check if ports 5000 and 3000 are free, otherwise release them.
3. Run docker file `sudo docker-compose up --build`
4. Navigate to localhost:3000 to classify new documents