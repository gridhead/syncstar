import { Button, Card, CardBody, ListGroup, Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import compdict from "../features/icon.jsx";
import { hidePicker, makeFileIden, makeFileName } from "../features/part.jsx";
import DemandDiskSync from "../features/sync.jsx";
import ListItemDisk from "./disk.jsx";
import ListItemFile from "./file.jsx";
import ListItem from "./item.jsx";

function SelectWindow({ show, pick, imejlist }) {
  const dispatch = useDispatch();
  const fileName = useSelector((area) => area.area.fileName);
  const disconnected = useSelector((area) => area.area.disconnected);
  const fileIden = useSelector((area) => area.area.fileIden);
  const diskIden = useSelector((area) => area.area.diskIden);

  function selectFile(fileiden, filename) {
    dispatch(makeFileIden(fileiden));
    dispatch(makeFileName(filename));
  }

  return (
    <Modal
      show={show}
      className="fade modal-lg modal-dialog-centered modal-dialog-scrollable"
      size="lg"
      centered={true}
      scrollable={true}
    >
      <Modal.Body>
        <h2 className="headelem mb-4 text-success" style={{ textAlign: "center" }}>
          Preparing
        </h2>
        <p style={{ textAlign: "center" }} className="strdelem">
          You have selected the following USB storage device.
        </p>
        <ListGroup className="strdelem mb-3">
          <ListItem
            key={pick.iden}
            name={`${pick.data.name.vendor} ${pick.data.name.handle}`}
            subs={<ListItemDisk size={pick.data.size} loca={pick.data.node} />}
            type={pick.iden}
            imej={compdict["device"]}
            action={false}
            suit="success"
          />
        </ListGroup>
        <p style={{ textAlign: "center" }} className="strdelem">
          Choose from the following images for synchronization.
        </p>
        <ListGroup className="strdelem mb-3">
          {Object.keys(imejlist).length > 0 ? (
            Object.entries(imejlist).map(([key, value]) => (
              <ListItem
                key={key}
                name={value.name}
                file={value.path}
                subs={
                  <ListItemFile
                    size={value.size}
                    suit={pick.data.size >= value.size ? "text-success" : "text-warning"}
                  />
                }
                type={Object.prototype.hasOwnProperty.call(compdict, value.type) ? value.type : "common"}
                imej={
                  Object.prototype.hasOwnProperty.call(compdict, value.type) ? compdict[value.type] : compdict["common"]
                }
                action={true}
                suit={pick.data.size >= value.size ? "success" : "warning"}
                activate={() => selectFile(key, value.name)}
              />
            ))
          ) : (
            <Card>
              <CardBody className="strdelem">No images detected</CardBody>
            </Card>
          )}
        </ListGroup>
        <ListGroup className="strdelem" style={{ textAlign: "center" }}>
          {fileName.trim() !== "" ? (
            <span>
              You have selected<h4 className="headelem">{fileName}</h4>
            </span>
          ) : (
            "No images selected"
          )}
        </ListGroup>
      </Modal.Body>
      <Modal.Footer className="justify-content-between">
        <Button variant="success" onClick={() => DemandDiskSync({ dispatch, fileIden, diskIden, disconnected })}>
          Sync
        </Button>
        <Button variant="danger" onClick={() => dispatch(hidePicker())}>
          Back
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default SelectWindow;
