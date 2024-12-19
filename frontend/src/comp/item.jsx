import { ListGroup } from "react-bootstrap";

function ListItem({ name, subs, type, imej, activate, action, suit }) {
  return (
    <ListGroup.Item className={`p-2 border-${suit}`} action={action} onClick={activate}>
      <div className="d-flex w-100" style={{ gap: "0.5rem" }}>
        <div style={{ aspectRatio: "1/1", height: "50px" }}>
          <img src={imej} className={`w-100 h-100 filter-${suit}`} />
        </div>
        <div className="d-flex flex-column flex-grow-1 text-truncate">
          <div className="d-flex justify-content-between align-items-start">
            <h5 className="mb-1 headelem" id="name-main-indx">
              {name}
            </h5>
            <span className={`badge text-bg-${suit} rounded-pill monotext`}>{type}</span>
          </div>
          {subs}
        </div>
      </div>
    </ListGroup.Item>
  );
}

export default ListItem;
