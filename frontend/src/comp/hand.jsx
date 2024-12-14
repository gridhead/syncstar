import { Card, CardBody, Container, ListGroup } from "react-bootstrap";
import { useSelector } from "react-redux";

import compdict from "../features/icon.jsx";
import ListItemFile from "./file.jsx";
import ListItem from "./item.jsx";

function HandList() {
  const fileDict = useSelector((area) => area.area.fileDict);

  return (
    <>
      <Container>
        <h2 className="headelem">Available</h2>
        <ListGroup>
          {Object.keys(fileDict).length > 0 ? (
            Object.entries(fileDict).map(([key, value]) => (
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
    </>
  );
}

export default HandList;
