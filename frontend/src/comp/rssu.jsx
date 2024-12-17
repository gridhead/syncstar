import { Accordion, ListGroup } from "react-bootstrap";

function FeedUnit({ data }) {
  return (
    <ListGroup.Item className="px-0">
      <span className="secotext px-2 text-success">
        From <span style={{ fontWeight: "bold" }}>{data.head}</span>
      </span>
      <hr className="my-2" />
      <Accordion defaultActiveKey="0" className="pb-2" flush>
        {Object.keys(data.data).length > 0 ? (
          Object.entries(data.data).map(([item, unit]) => (
            <Accordion.Item key={item} eventKey={item}>
              <Accordion.Header>
                <span className="text-truncate">{unit.head}</span>
              </Accordion.Header>
              <Accordion.Body>
                <a className="secotext" href={unit.link} target="_blank" rel="noopener noreferrer">
                  {unit.date}
                </a>
                <br />
                {unit.summ}
              </Accordion.Body>
            </Accordion.Item>
          ))
        ) : (
          <Accordion.Item eventKey="0">
            <Accordion.Header>No entries available</Accordion.Header>
            <Accordion.Body>
              <a
                className="secotext"
                href="https://github.com/gridhead/syncstar/commit/48b9f3d73f29494f0f73b6888ce9c4533b9ba6be"
                target="_blank"
                rel="noopener noreferrer"
              >
                Tue, 14 May 2024 06:59:00 GMT +05:30
              </a>
              <br />
              White it is likely that the provided feed resource is valid and has no entries within it, you would still
              want to check out the configuration for the provided feed resources to ensure that things are working as
              expected, once you are sure that there are no ongoing synchronizations.
            </Accordion.Body>
          </Accordion.Item>
        )}
      </Accordion>
    </ListGroup.Item>
  );
}

export default FeedUnit;
