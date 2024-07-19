import React, { useState } from 'react';
import './App.css';
//import axios from 'axios';

function App() {
  const [userInput, setUserInput] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchRecommendations = async () => {
    setError(null);
    
    // Check if user input is empty
    if (!userInput.trim()) {
      setError('Please enter a topic or preference.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      // Replace this URL with the actual URL of your AWS Lambda function
      const response = await fetch('https://msgomewthi.execute-api.us-east-1.amazonaws.com/dev/bookrecomm',{
        method:'POST',
        body: JSON.stringify({"topic": userInput}),
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const reader = response.body.getReader();
      const stream = new ReadableStream({
          start(controller) {
              function push() {
                  reader.read().then(({ done, value }) => {
                      if (done) {
                          controller.close();
                          return;
                      }
                      controller.enqueue(value);
                      push();
                  });
              }
              push();
          }
      });

      const result = await new Response(stream).text();
      const data = JSON.parse(result);
      // Update the recommendations state with the data returned from Lambda
      setRecommendations(data); // Assuming Lambda returns an object with 'recommendations' field
    } catch (err) {
      console.log(err)
      setError('Error fetching recommendations.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Book Recommendations</h1>
      <textarea
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder='Enter your feelings or preferences, e.g., "I want a thrilling mystery with a twist ending."'
      />
      <button onClick={fetchRecommendations}>Get Recommendations</button>
      {loading && <p className="loading">Loading...</p>}
      {error && <p className="error">{error}</p>}
      {recommendations.length > 0 && (
        <div className="recommendations">
          <h2>Recommended Books:</h2>
          <ul>
            {recommendations.map((book, index) => (
              <li key={index}>{book}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
