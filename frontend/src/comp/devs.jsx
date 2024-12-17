import { Card, CardBody, ListGroup } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import compdict from "../features/icon.jsx";
import { makeDevsPick, makeDiskIden, makeFileIden, makeFileName, showPicker } from "../features/part.jsx";
import ListItemDisk from "./disk.jsx";
import ListItem from "./item.jsx";

function DeviceList() {
  const dispatch = useDispatch();
  const devsDict = useSelector((area) => area.area.devsDict);

  function handleShow(iden, data) {
    dispatch(makeDevsPick({ iden: iden, data: data }));
    dispatch(makeFileName(""));
    dispatch(makeDiskIden(iden));
    dispatch(showPicker());
    dispatch(makeFileIden(""));
  }

  return (
    <>
      <h2 className="headelem">Pending</h2>
      <ListGroup>
        {Object.keys(devsDict).length > 0 ? (
          Object.entries(devsDict).map(([key, value]) => (
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
    </>
  );
}

export default DeviceList;
