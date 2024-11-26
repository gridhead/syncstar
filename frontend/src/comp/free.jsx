import { Modal } from "react-bootstrap";

function SevereWindow({ show }) {
  return (
    <Modal show={show} className="fade" size="lg" centered={true}>
      <Modal.Body>
        <h2 className="headelem mb-4 text-danger" style={{ textAlign: "center" }}>
          Disconnected
        </h2>
        <p className="strdelem mb-0" style={{ textAlign: "center" }}>
          Please refresh your current browser window to reestablish the connection to the service.
        </p>
      </Modal.Body>
    </Modal>
  );
}

export default SevereWindow;
