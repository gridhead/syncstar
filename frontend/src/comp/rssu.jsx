import { Accordion, Badge, ListGroup } from "react-bootstrap";

import QRCodeOver from "./code.jsx";

function FeedUnit({ data, link }) {
  const burl = new URL(link);
  const base = burl.origin;

  return (
    <ListGroup.Item className="px-0 pb-0" variant="secondary">
      <div className="px-2 d-flex justify-content-between align-items-start">
        <span className="secotext">
          From <span style={{ fontWeight: "bold" }}>{data.head}</span>
        </span>
        <Badge
          bg="secondary"
          className="monotext"
          as="a"
          href={base}
          target="_blank"
          rel="noopener noreferrer"
          pill={true}
        >
          {Object.keys(data.data).length} entries
        </Badge>
      </div>
      <hr className="mt-1 mb-0" />
      <Accordion defaultActiveKey="0" flush>
        {Object.keys(data.data).length > 0 ? (
          Object.entries(data.data).map(([item, unit]) => (
            <Accordion.Item key={item} eventKey={item}>
              <Accordion.Header>
                <span className="text-truncate" style={{ fontWeight: "bold" }}>
                  {unit.head}
                </span>
              </Accordion.Header>
              <Accordion.Body>
                <QRCodeOver head={unit.head} link={unit.link}>
                  <a className="secotext text-success" href={unit.link} target="_blank" rel="noopener noreferrer">
                    {unit.date}
                  </a>
                </QRCodeOver>
                <br />
                <span>{unit.summ}</span>
              </Accordion.Body>
            </Accordion.Item>
          ))
        ) : (
          <Accordion.Item eventKey="0">
            <Accordion.Header>No entries available</Accordion.Header>
            <Accordion.Body>
              <a
                className="secotext text-success"
                href="https://github.com/gridhead/syncstar/commit/48b9f3d73f29494f0f73b6888ce9c4533b9ba6be"
                target="_blank"
                rel="noopener noreferrer"
              >
                Tue, 14 May 2024 06:59:00 GMT +05:30
              </a>
              <br />
              White it is likely that the provided feed resources is valid and has no entries within it, you would still
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
