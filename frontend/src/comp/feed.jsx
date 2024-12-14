import { Card, CardBody, Container, ListGroup } from "react-bootstrap";

function FeedUnit() {
  return (
    <>
      <Container className="mt-4">
        <h2 className="headelem">Information</h2>
        <ListGroup>
          <Card>
            <CardBody className="strdelem">No source detected</CardBody>
          </Card>
        </ListGroup>
      </Container>
    </>
  );
}

export default FeedUnit;
