import axios from "axios";
import "./App.css";
import { useState } from "react";

function App() {
  const [state, setState] = useState({ output: "", imgUrl: "" });

  const handleUploadImage = async (ev) => {
    ev.preventDefault();

    const data = new FormData();
    data.append("file", ev.target.files[0]);
    data.append("filename", ev.target.files[0].name);
    let output = await axios({
      url: "https://anpr-ocr.onrender.com/extract",
      data,
      method: "post",
    });
    setState((prev) => {
      return {
        ...prev,
        imgUrl: URL.createObjectURL(ev.target.files[0]),
        output: output.data,
      };
    });
  };

  const getOutputScreen = () => {
    return (
      <>
        <div className="child">
          <img alt="preview image" src={state.imgUrl} />
        </div>
        <div className="child">Predicted value:<b>{state.output}</b></div>
      </>
    );
  };
  return (
    <div className="parent">
      <div className="child">
        <input type="file" onChange={handleUploadImage} />
      </div>
      {state.output && getOutputScreen()}
    </div>
  );
}

export default App;
