import { QRCodeCanvas } from "qrcode.react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";

function QRCodeOver({ head, children, link }) {
  return (
    <OverlayTrigger
      placement="bottom"
      overlay={
        <Tooltip>
          <QRCodeCanvas
            value={link}
            size={185}
            bgColor="rgba(0, 0, 0, 0)"
            level="L"
            marginSize={1}
            title={head}
            className="filter-success"
          />
        </Tooltip>
      }
    >
      {children}
    </OverlayTrigger>
  );
}

export default QRCodeOver;
