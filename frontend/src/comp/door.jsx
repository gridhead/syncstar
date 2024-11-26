import { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { Form } from "react-bootstrap";
import { useDispatch } from "react-redux";

import { hideSignIn, makeNotifyKlas, makeNotifyText, pushNotification } from "../features/part.jsx";

function SignInWindow({ show }) {
  const dispatch = useDispatch();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function SignIn() {
    if (username.trim() === "" || password.trim() === "") {
      return;
    }

    try {
      const response = await fetch("/sign", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          username: username,
          password: password,
        },
        credentials: "include",
      });

      if (response.ok) {
        dispatch(makeNotifyText("Welcome to SyncStar"));
        dispatch(makeNotifyKlas("success"));
        dispatch(pushNotification());
      } else {
        dispatch(makeNotifyText("Please check your credentials before trying again"));
        dispatch(makeNotifyKlas("warning"));
        dispatch(pushNotification());
      }
    } catch (expt) {
      console.error("Exception occurred", expt);
      dispatch(makeNotifyText("Please check your connection before trying again"));
      dispatch(makeNotifyKlas("danger"));
      dispatch(pushNotification());
    }
    dispatch(hideSignIn());
  }

  const returnSubmit = async (item) => {
    if (item.key === "Enter") {
      await SignIn();
    }
  };

  return (
    <Modal show={show} className="fade" size="md" centered={true}>
      <Modal.Body>
        <h2 className="headelem mb-4 text-success" style={{ textAlign: "center" }}>
          SyncStar
        </h2>
        <p className="strdelem mb-3" style={{ textAlign: "center" }}>
          Please sign in to continue
        </p>
        <Form.Control
          type="email"
          placeholder="Username"
          id="username"
          className="mb-3"
          aria-describedby="Username"
          onChange={(item) => setUsername(item.target.value)}
          onKeyDown={returnSubmit}
        />
        <Form.Control
          type="password"
          placeholder="Password"
          id="password"
          className="mb-3"
          aria-describedby="Password"
          onChange={(item) => setPassword(item.target.value)}
          onKeyDown={returnSubmit}
        />
        <div className="d-grid">
          <Button variant="success" style={{ textAlign: "center" }} onClick={() => SignIn()}>
            Sign in
          </Button>
        </div>
      </Modal.Body>
    </Modal>
  );
}

export default SignInWindow;
