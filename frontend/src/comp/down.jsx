import { Container, Navbar } from "react-bootstrap";
import { useDispatch } from "react-redux";

import { makeNotifyKlas, makeNotifyText, pushNotification } from "../features/part.jsx";

function BottomNavbar({ timedata }) {
  const dispatch = useDispatch();

  async function MakeExit() {
    try {
      const response = await fetch("/exit", {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        dispatch(makeNotifyText("Please sign in to continue"));
        dispatch(makeNotifyKlas("warning"));
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
  }

  return (
    <Navbar className="fixed-bottom bg-body-secondary">
      <Container>
        <a className="navbar-text" href="#" onClick={() => MakeExit()}>
          Logout
        </a>
        <span className="navbar-text strdelem" id="lastupdt">
          Last updated on {timedata ? timedata : "00:00:00 00/00/00 UTC"}
        </span>
      </Container>
    </Navbar>
  );
}

export default BottomNavbar;
