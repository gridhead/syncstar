import { Toast, ToastContainer } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import { pullNotification } from "../features/part.jsx";

function Notify({ text, show }) {
  const dispatch = useDispatch();
  const notifyKlas = useSelector((area) => area.area.notifyKlas);

  return (
    <ToastContainer position="bottom-center" className="p-4">
      <Toast
        className={`align-items-center border-0 p-0 text-bg-${notifyKlas}`}
        style={{ width: "fit-content" }}
        show={show}
        onClose={() => dispatch(pullNotification())}
        delay={2500}
        autohide={true}
      >
        <Toast.Body style={{ textAlign: "center" }}>{text}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default Notify;
