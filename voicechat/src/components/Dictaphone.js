import React, { useEffect, useState } from "react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import axios from "axios";

const Dictaphone = () => {
    const {
        listening,
        interimTranscript,
        finalTranscript,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();
    const [transcript, setTranscript] = useState("");
    const [response, setResponse] = useState("");

    const generateResponse = async (input) => {
        let reply;
        try {
            const response = await axios.post('http://localhost:8000/generate', {
                query: input
            });
            reply = response.data.generated_text;
        }
        catch (error){
            reply = "Error generating text";
            console.log(error);
        }
        setResponse(reply);
        speak(reply);
    };
    useEffect(() => {
        if(transcript!==""){
            generateResponse(transcript);
        }
    }, [transcript]);
    
    if(!browserSupportsSpeechRecognition) {
        return <span>Browser doesn't support speech recognition.</span>;
    }


    const startListening = () => {
        SpeechRecognition.startListening({ continuous: true });
    };

    const stopListening = () => {
        SpeechRecognition.stopListening();
        setTranscript(finalTranscript);
        resetTranscript();
    };


    
    const speak = (text) => {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US';
        speech.pitch = 1;
        speech.rate = 1;
        window.speechSynthesis.speak(speech);
    }

    return (
        <div>
            <div className="controls">
                <p>Microphone: {listening? "on": "off"}</p>
                <button onClick={startListening}>Speak</button>
                <button onClick={stopListening}>Stop</button>
                <button onClick={resetTranscript}>Reset</button>
                <p>Interim Transcript: {interimTranscript}</p>
                <p>Final Transcript: {finalTranscript}</p>
                <p>Question: {transcript}</p>
                <p>Response: {response}</p>
            </div>
        </div>
    )
};

export default Dictaphone;
