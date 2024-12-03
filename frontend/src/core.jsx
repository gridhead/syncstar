import { useEffect, useState } from "react";
import { Accordion, Card, CardBody, Container, ListGroup } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import packInfo from "../package.json";
import ListItemDisk from "./comp/disk.jsx";
import SignInWindow from "./comp/door.jsx";
import BottomNavbar from "./comp/down.jsx";
import ListItemFile from "./comp/file.jsx";
import SevereWindow from "./comp/free.jsx";
import ListItem from "./comp/item.jsx";
import Notify from "./comp/note.jsx";
import MainNavbar from "./comp/peak.jsx";
import SelectWindow from "./comp/talk.jsx";
import ListItemTask from "./comp/task.jsx";
import { logodict, mooddict } from "./features/dict.jsx";
import compdict from "./features/icon.jsx";
import {
  hidePicker,
  hideSignIn,
  makeDiskIden,
  makeFileIden,
  makeFileName,
  pullDisconnect,
  pushDisconnect,
  showPicker,
  showSignIn,
} from "./features/part.jsx";

function Main() {
  const dispatch = useDispatch();

  const [filedict, setFileDict] = useState({});
  const [timedata, setTimeData] = useState("");
  const [devsdict, setDevsDict] = useState({});
  const [jobsdict, setJobsDict] = useState({});
  const [jsondata, setJSONData] = useState(null);
  const [devsPick, setDevsPick] = useState({
    iden: "",
    data: { iden: 0, name: { handle: "", vendor: "" }, node: "", size: 0 },
  });

  const testcont = useSelector((area) => area.area.value);
  const pickerVisual = useSelector((area) => area.area.pickerVisual);
  const signinVisual = useSelector((area) => area.area.signinVisual);
  const notifyVisual = useSelector((area) => area.area.notifyVisual);
  const notifyText = useSelector((area) => area.area.notifyText);
  const disconnected = useSelector((area) => area.area.disconnected);

  function handleShow(iden, data) {
    setDevsPick({ iden: iden, data: data });
    dispatch(makeFileName(""));
    dispatch(makeDiskIden(iden));
    dispatch(showPicker());
    dispatch(makeFileIden(""));
  }

  useEffect(() => {
    const intervalId = setInterval(() => {
      try {
        fetch("/read", { method: "GET", credentials: "include" }).then(async (response) => {
          if (response.status === 200) {
            let data = await response.json();
            setJSONData(JSON.stringify(data, null, 2));
            setFileDict(data.file);
            setTimeData(data.time);
            setDevsDict(data.devs);
            setJobsDict(data.jobs);
            dispatch(pullDisconnect());
            dispatch(hideSignIn());
          } else if (response.status === 401) {
            dispatch(pullDisconnect());
            dispatch(showSignIn());
            dispatch(hidePicker());
          } else {
            dispatch(pushDisconnect());
            dispatch(hideSignIn());
            dispatch(hidePicker());
          }
        });
      } catch (expt) {
        console.error("Exception occurred", expt);
        dispatch(pushDisconnect());
        dispatch(hideSignIn());
        dispatch(hidePicker());
      }
    }, 1000);
    return () => clearInterval(intervalId);
  }, [dispatch]);

  useEffect(() => {
    document.title = `SyncStar v${packInfo.version}`;
  }, []);

  return (
    <>
      <MainNavbar />
      <Container>
        <h2 className="headelem">Available {testcont}</h2>
        <ListGroup>
          {Object.keys(filedict).length > 0 ? (
            Object.entries(filedict).map(([key, value]) => (
              <ListItem
                key={key}
                name={value.name}
                subs={<ListItemFile size={value.size} suit="" />}
                type={Object.prototype.hasOwnProperty.call(compdict, value.type) ? value.type : "common"}
                imej={
                  Object.prototype.hasOwnProperty.call(compdict, value.type) ? compdict[value.type] : compdict["common"]
                }
                activate={null}
                action={false}
                suit="secondary"
              />
            ))
          ) : (
            <Card>
              <CardBody className="strdelem">No images detected</CardBody>
            </Card>
          )}
        </ListGroup>
      </Container>
      <Container className="mt-4">
        <h2 className="headelem">Pending</h2>
        <ListGroup>
          {Object.keys(devsdict).length > 0 ? (
            Object.entries(devsdict).map(([key, value]) => (
              <ListItem
                key={key}
                name={`${value.name.vendor} ${value.name.handle}`}
                subs={<ListItemDisk size={value.size} loca={value.node} />}
                type={key}
                imej={compdict["device"]}
                activate={() => handleShow(key, value)}
                action={true}
                suit="secondary"
              />
            ))
          ) : (
            <Card>
              <CardBody className="strdelem">No devices detected</CardBody>
            </Card>
          )}
        </ListGroup>
      </Container>
      <Container className="mt-4">
        <h2 className="headelem">Progress</h2>
        <ListGroup>
          {Object.keys(jobsdict).length > 0 ? (
            Object.entries(jobsdict).map(([key, value]) => (
              <ListItem
                key={key}
                name={value.isos}
                subs={<ListItemTask mood={value.mood} loca={value.disk} time={value.time} rcrd={value.rcrd} />}
                type={key}
                imej={logodict[value.mood]}
                action={false}
                suit={mooddict[value.mood]}
              />
            ))
          ) : (
            <Card>
              <CardBody className="strdelem">No running synchronizations detected</CardBody>
            </Card>
          )}
        </ListGroup>
      </Container>
      <Container className="mt-4">
        <h2 className="headelem">Diagnosis</h2>
        <ListGroup>
          <Accordion>
            <Accordion.Item eventKey={0}>
              <Accordion.Header>Expand</Accordion.Header>
              <Accordion.Body>
                <pre id="debplc" className="mb-0">
                  {jsondata ? jsondata : "Debug information goes here"}
                </pre>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </ListGroup>
      </Container>
      <SelectWindow show={pickerVisual} pick={devsPick} imejlist={filedict} />
      <SignInWindow show={signinVisual} />
      <SevereWindow show={disconnected} />
      <Notify text={notifyText} show={notifyVisual} />
      <BottomNavbar timedata={timedata} />
    </>
  );
}

export default Main;
