import { useEffect, useState } from "react";
import { Card, CardBody, ListGroup } from "react-bootstrap";

import FeedUnit from "./rssu.jsx";

function FeedList() {
  const [feedData, makeFeedData] = useState({});

  useEffect(() => {
    const fetchRSS = async () => {
      try {
        const response = await fetch("/news", { method: "GET", credentials: "include" });
        if (response.status === 200) {
          const data = await response.json();
          makeFeedData(data.data);
        }
      } catch (expt) {
        console.error("Exception occurred", expt);
      }
    };

    fetchRSS();
    const intervalId = setInterval(fetchRSS, 30000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <h2 className="headelem">Highlights</h2>
      <ListGroup>
        {Object.keys(feedData).length > 0 ? (
          Object.entries(feedData).map(([item, data]) => <FeedUnit key={item} data={data} />)
        ) : (
          <Card>
            <CardBody className="strdelem">No source detected</CardBody>
          </Card>
        )}
      </ListGroup>
    </>
  );
}

export default FeedList;
