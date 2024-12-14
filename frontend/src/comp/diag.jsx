import { Accordion, Container, ListGroup } from "react-bootstrap";
import { useSelector } from "react-redux";

function RepairArea() {
  const jsonData = useSelector((area) => area.area.jsonData);

  return (
    <Container className="mt-4">
      <h2 className="headelem">Diagnosis</h2>
      <ListGroup>
        <Accordion>
          <Accordion.Item eventKey={0}>
            <Accordion.Header>Expand</Accordion.Header>
            <Accordion.Body>
              <pre id="debplc" className="mb-0">
                {jsonData ? jsonData : "Debug information goes here"}
              </pre>
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
      </ListGroup>
    </Container>
  );
}

export default RepairArea;
