import React from "react";
import { useState, useEffect } from "react";

function SimilarSongs(props) {
  const [songs, setSimilarSongs] = useState({});

  //triggered whenever props changes
  useEffect(() => {
    fetch("/api/songs/similar")
      .then((res) => res.json())
      .then(
        (result) => {
          console.log("setting initial state of recommended songs");
          setSimilarSongs(result);
          // console.log(result);
        },
        (error) => {
          console.log(error);
        }
      );
  }, []);

  //style for SimilarSongs component
  let divStyle = {
    padding: "10px",
    textAlign: "center",
    width: "fit-content",
    position: "absolute",
    right: "150px",
    top: "50px",
    display: "inline-block",
  };
  return (
    <div className="border border-dark" style={divStyle}>
      <h1>Similar</h1>
      <div>
        {Object.keys(songs).map((name, i) => (
          <p key={i} className="border-bottom">
            <a href={songs[name]} target="_blank" rel="noreferrer">
              {name}
            </a>
          </p>
        ))}
      </div>
    </div>
  );
}

export default SimilarSongs;
