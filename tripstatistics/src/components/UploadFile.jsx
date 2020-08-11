import React, { useState } from "react";

export default function UploadFile() {
  // State Hook
  const [selectedFile, setSelectedFile] = useState(null);

  // On file select (from the pop up)
  const onFileChange = (event) => {
    // Update the state
    setSelectedFile(event.target.files[0]);
  };

  // On file upload (click the upload button)
  const onFileUpload = (event) => {
    event.preventDefault();

    // Details of the uploaded file
    console.log(selectedFile);

    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append("myFile", selectedFile, selectedFile.name);

    // Request made to the backend api
    // Send formData object
    // axios.post("api/uploadfile", formData);
  };

  // File content to be displayed after
  // file upload is complete
  const fileData = () => {
    if (selectedFile) {
      console.log(`fileData -> selectedFile`, selectedFile);

      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {selectedFile.name}</p>
          <p>File Type: {selectedFile.type}</p>
          <p>Last Modified: {selectedFile.lastModifiedDate.toDateString()}</p>
          <p>Size: {(selectedFile.size / 1024).toFixed(3)} KiB</p>
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  };

  return (
    <div>
      <h1>Upload File</h1>
      <form action=''>
        <input
          type='file'
          onChange={(e) => {
            onFileChange(e);
          }}
        />
        <button
          type='submit'
          onClick={(e) => {
            onFileUpload(e);
          }}
        >
          Upload
        </button>
      </form>
      {fileData()}
    </div>
  );
}

/* 
Sources: 

https://www.geeksforgeeks.org/file-uploading-in-react-js/

*/
