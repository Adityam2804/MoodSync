import React from "react";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import Songs from "./Songs";
import { Fragment } from "react";

function Chat() {
  const [chatHistory, setChatHistory] = useState(
    JSON.parse(sessionStorage.getItem("chatHistory")) || [] // Initialize with sessionStorage data if available
  );
  const [chatResponse, setChatResponse] = useState("");
  const [chatTone, setChatTone] = useState("Joy");
  const [songs, setSongs] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const textAreaRef = useRef();
  let chat = "";

  useEffect(() => {
    // Store chat history in sessionStorage whenever it changes
    sessionStorage.setItem("chatHistory", JSON.stringify(chatHistory));
  }, [chatHistory]);

  function handleTextArea(e) {
    chat = e.target.value;
  }

  function chatHandler(chat) {
    if (chat.length === 0) {
      return;
    }
    setIsLoading(true);
    textAreaRef.current.value = "";
    getTone(chat);
    getResponse(chat, chatTone);
    updateChatHistory(chat, "user");
    setChatResponse("");
  }

  function updateChatHistory(message, sender) {
    setChatHistory((prevHistory) => [
      ...prevHistory,
      { text: message, sender: sender },
    ]);
  }

  function getTone(chat) {
    axios
      .post("/api/tone", {
        chat: chat,
      })
      .then(function (response) {
        let tone = response.data.tone;
        if (tone !== chatTone) {
          console.log("Tone changes from ", chatTone, " to ", tone);
          setChatTone(tone);
          getSongs(tone);
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function getSongs(tone) {
    axios
      .post("/api/songs", {
        tone: tone,
      })
      .then(function (response) {
        setSongs(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function getResponse(chat, tone) {
    axios
      .post("/api/chat", {
        chat: chat,
        tone: tone,
      })
      .then(function (response) {
        let res = response.data.response;
        setChatResponse(res);
        updateChatHistory(res, "bot"); // Append response to chat history as bot message
      })
      .catch(function (error) {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }

  let divStyle = {
    padding: "10px",
    top: "50px",
    textAlign: "center",
    align: "center",
    width: "45%",
    position: "absolute",
    left: "28%",
    display: "inline-block",
  };

  let userMessageStyle = {
    textAlign: "right",
    backgroundColor: "#dcf8c6",
    padding: "8px",
    borderRadius: "10px",
    margin: "5px",
    maxWidth: "60%",
    alignSelf: "flex-end",
    clear: "both",
  };

  let botMessageStyle = {
    textAlign: "left",
    backgroundColor: "#dcf8f3",
    padding: "8px",
    borderRadius: "10px",
    margin: "5px",
    maxWidth: "60%",
    alignSelf: "flex-start",
    clear: "both",
  };

  return (
    <Fragment>
      <div style={divStyle}>
        <h2 id="tone">{chatTone}</h2>
        <hr style={{ backgroundColor: "#002000", height: 0.2 }} />
        <br />
        <div style={{ display: "flex", flexDirection: "column" }}>
          {chatHistory.map((item, index) => (
            <div
              key={index}
              style={
                item.sender === "user" ? userMessageStyle : botMessageStyle
              }
            >
              {item.text}
            </div>
          ))}
        </div>
        {isLoading && <div>Loading...</div>}
        <div
          style={{ paddingTop: "20px", paddingBottom: "10px", display: "flex" }}
        >
          <textarea
            ref={textAreaRef}
            id="chatbox"
            rows="2"
            cols="80"
            onChange={handleTextArea}
          ></textarea>
          <button
            className="btn btn-success ml-2"
            onClick={() => chatHandler(chat)}
          >
            Send
          </button>
        </div>
      </div>
      <Songs songs={songs} />
    </Fragment>
  );
}

export default Chat;
