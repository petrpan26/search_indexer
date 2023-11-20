
# Question and Answering Demo with Next.js and Python
This is a demo application that demonstrates a Question and Answering (Q&A) system using Next.js for the frontend and Python with FastAPI for the backend. This README provides instructions on how to set up and run the application.'

Blog: https://medium.com/p/21823684dfb2

## Prerequisites
Before you can run the demo, make sure you have the following software installed on your system:

- Node.js and Yarn: You can download Node.js from nodejs.org and install Yarn globally using npm by running npm install -g yarn.

- Python: You'll need Python 3.x installed on your system. You can download it from python.org.

## Getting Started
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/qa-demo.git
```
Replace yourusername with your actual GitHub username or the URL of the repository.

Navigate to the project directory:

```bash
cd qa-demo
```
Install frontend dependencies. Run the following command in the project root directory:

```bash
yarn install
```
Install backend dependencies. Navigate to the backend directory:

```bash
cd backend
```
Run the following command:

```bash
pip install -r requirements.txt
```
Running the Application
### Backend (Python with FastAPI)
Run the following command to start the FastAPI server:

```bash
yarn fastapi-dev
```
This will launch the backend server, which will be accessible at http://localhost:8000.

### Frontend (Next.js)
In the project root directory, run the following command to start the Next.js development server:

```bash
yarn next-dev
```
The frontend server will start and the application will be accessible at http://localhost:3000.

Open your web browser and navigate to http://localhost:3000 to use the Q&A system.

## Usage
Once the application is up and running, you can use the Q&A system to ask questions and get answers based on the provided dataset or model. Follow the on-screen instructions to interact with the application.

## Contributing
If you'd like to contribute to this demo, please fork the repository, make your changes, and create a pull request. We welcome contributions and improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
This demo was built using Next.js for the frontend and FastAPI for the backend.
Special thanks to the contributors of the open-source libraries used in this project.
Feel free to reach out if you have any questions or need further assistance!
