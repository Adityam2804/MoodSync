import React from "react";
import { useState, useRef } from "react";
import axios from "axios";
import Songs from "./Songs";
import { Fragment } from "react";

function Chat() {
  const [chatResponse, setChatResponse] = useState("");
  const [chatTone, setChatTone] = useState("Joy");
  const [songs, setSongs] = useState({});
  const [isLoading, setIsLoading] = useState(false); // Loading state for chat response
  const textAreaRef = useRef();
  let chat = "";

  function handleTextArea(e) {
    chat = e.target.value;
  }

  function chatHandler(chat) {
    if (chat.length === 0) {
      return;
    }
    setIsLoading(true); // Start loading
    textAreaRef.current.value = "";
    getTone(chat);
    getResponse(chat, chatTone);
    setChatResponse("");
  }

  function getTone(chat) {
    axios
      .post("/api/tone", {
        chat: chat,
      })
      .then(function (response) {
        let tone = response["data"]["tone"];
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
        setSongs(response["data"]);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function getResponse(chat, tone) {
    console.log("in getResponse");
    console.log(tone);
    axios
      .post("/api/chat", {
        chat: chat,
        tone: tone,
      })
      .then(function (response) {
        let res = response["data"]["response"];
        setChatResponse(res);
      })
      .catch(function (error) {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false); // End loading
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

  return (
    <Fragment>
      <div style={divStyle}>
        <h2 id="tone">{chatTone}</h2>
        <hr
          style={{
            backgroundColor: "#002000",
            height: 0.2,
          }}
        />
        <br />
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <div style={{ wordWrap: "break-word" }}>{chatResponse}</div>
        )}
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
