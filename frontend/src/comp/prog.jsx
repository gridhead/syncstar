import { Card, CardBody, Container, ListGroup } from "react-bootstrap";
import { useSelector } from "react-redux";

import { logodict, mooddict } from "../features/dict.jsx";
import ListItem from "./item.jsx";
import ListItemTask from "./task.jsx";

function ProgressList() {
  const jobsDict = useSelector((area) => area.area.jobsDict);

  return (
    <>
      <Container className="mt-4">
        <h2 className="headelem">Progress</h2>
        <ListGroup>
          {Object.keys(jobsDict).length > 0 ? (
            Object.entries(jobsDict).map(([key, value]) => (
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
    </>
  );
}

export default ProgressList;
