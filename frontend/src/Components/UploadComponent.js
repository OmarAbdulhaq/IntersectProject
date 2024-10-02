import React, { useState } from 'react';
import './UploadComponent.css';

const UploadComponent = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log("Extracted Data:", data);
            setResult(data.extracted_entities);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    const renderSection = (title, sectionData) => {
        return (
            <div className="section-container">
                <h5 className="section-title">{title}</h5>
                {typeof sectionData === 'object' && !Array.isArray(sectionData) ? (
                    Object.entries(sectionData).map(([key, value], index) => (
                        <p key={index}>
                            <strong>{key}:</strong> {value}
                        </p>
                    ))
                ) : Array.isArray(sectionData) ? (
                    sectionData.map((item, index) => (
                        <div key={index} className="sub-container">
                            {Object.entries(item).map(([key, value], idx) => (
                                <p key={idx}>
                                    <strong>{key}:</strong> {value}
                                </p>
                            ))}
                        </div>
                    ))
                ) : (
                    <p>{sectionData}</p>
                )}
            </div>
        );
    };

    return (
        <div className="upload-box">
            <h3>Upload PDF or DOCX</h3>
            <input type="file" onChange={handleFileChange} accept=".pdf,.docx" />
            <button onClick={handleUpload}>Upload</button>
            
            {result && (
                <div className="result-box">
                    <h4>Summary:</h4>
                    {renderSection("Personal Information", result["Personal Information"])}
                    {renderSection("Education", result.Education)}
                    {renderSection("Work Experience", result["Work Experience"])}
                </div>
            )}
        </div>
    );
};

export default UploadComponent;
