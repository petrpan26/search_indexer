'use client';
import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Box,
} from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import { DropzoneOptions, useDropzone } from 'react-dropzone';
import PDFViewer from './PDFViewer'; // Import the PDFViewer component
import axios from 'axios';

const SERVER_URL = process.env.SERVER_URL;

const DocumentUploader: React.FC = () => {
  const http = axios.create({
    baseURL: SERVER_URL,
    headers: {
      "Content-type": "application/json",
    },
  });
  http.get('/');
  console.log(SERVER_URL);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [newQuestion, setNewQuestion] = useState<string>('What is the relationship between Harry Potter and Malfoy ?');
  const [answer, setNewAnswer] = useState<string>(`Harry Potter and Malfoy have a hostile relationship. 
  Malfoy is portrayed as a mean and arrogant character who looks down on Harry and his friends. 
  He tries to belittle Harry by making fun of his family and offering to help him avoid making friends with the "wrong sort."
   Harry, on the other hand, is not intimidated by Malfoy and stands up to him. They have a confrontation and agree to have a wizard's duel later on.`);
  const [currentDocId, setDocId] = useState<string>("fd4e565a-7c66-4abf-8c97-6252b303893d");
  const [error, setError] = useState<string>('');

  const onDrop: DropzoneOptions['onDrop'] = (acceptedFiles, fileRejections) => {
    // Assuming only one file is allowed to be uploaded
    const file = acceptedFiles[0];
    http.post("/api/upload_document", {file: file}, {
      headers: {
        "Content-Type": "multipart/form-data",
      }
    }).then((response) => {

      setUploadedFile(file);
      setDocId(response.data.document_id);
    }, (error) => {
      if (axios.isAxiosError(error))  {
        // Access to config, request, and response
        setUploadedFile(null);
        setError(error.response?.data)
      } else {
        // Just a stock error
      }
    });

  };

  const handleQuestionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewQuestion(e.target.value);
  };

  const handleAddQuestion = () => {
    if (newQuestion.trim() !== '') {

      http.post("/api/answer_question", {document_id: currentDocId, question: newQuestion}, {
        headers: {
          "Content-Type": "application/json",
        }
      }).then((response) => {
        setNewAnswer(response.data.answer)
      }, (error) => {
        if (axios.isAxiosError(error))  {
          // Access to config, request, and response
          setError(error.response?.data)
        } else {
          // Just a stock error
        }
      });
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'application/pdf':      ['.pdf']
     }, // Add the accepted file types here,
     maxFiles: 1,
     maxSize: 5e6
  });

  return (
    <Container maxWidth="sm" style={containerStyle}>
      <Paper elevation={3} style={paperStyle}>
        <Typography variant="h4" gutterBottom style={titleStyle}>
          Your Personal Book Reading Bot
        </Typography>
        <Box {...getRootProps()} style={dropzoneStyle}>
          <input {...getInputProps()} />
          <CloudUploadIcon style={uploadIconStyle} />
          <Typography variant="h6" style={uploadText}>
            Drag & Drop or Click to Upload a Document (PDF)
          </Typography>
          {uploadedFile && <p>Uploaded: {uploadedFile.name}</p>}
        </Box>
      </Paper>
      {/* Display the PDFViewer component */}
      <PDFViewer file={uploadedFile}   />
      <Paper elevation={3} style={paperStyle}>
        <TextField
          fullWidth
          label="Ask a Question"
          variant="outlined"
          value={newQuestion}
          onChange={handleQuestionChange}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleAddQuestion}
          style={addButtonStyle}
        >
          Ask Question
        </Button>
      </Paper>
      <Paper elevation={3} style={paperStyle}>
          <Typography variant="body1" style={questionStyle}>
            <b>Question:</b> {newQuestion}
            <br></br>
            <b>Answer:</b> {answer}
          </Typography>
      </Paper>
    </Container>
  );
};

const containerStyle: React.CSSProperties = {
  backgroundColor: '#f5f5f5',
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
};

const paperStyle: React.CSSProperties = {
  padding: '20px',
  marginBottom: '20px',
  backgroundColor: 'white',
};

const titleStyle: React.CSSProperties = {
  textAlign: 'center',
  marginBottom: '20px',
  color: '#2196f3',
};

const dropzoneStyle: React.CSSProperties = {
  border: '2px dashed #cccccc',
  borderRadius: '4px',
  textAlign: 'center',
  padding: '20px',
  cursor: 'pointer',
};

const uploadIconStyle: React.CSSProperties = {
  fontSize: 80,
  marginBottom: '10px',
  color: '#2196f3',
};

const uploadText: React.CSSProperties = {
  marginBottom: '10px',
  color: '#666',
};

const addButtonStyle: React.CSSProperties = {
  marginTop: '10px',
};

const questionStyle: React.CSSProperties = {
  marginBottom: '10px',
};

export default DocumentUploader;
