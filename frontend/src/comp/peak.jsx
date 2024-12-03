import { Container, Navbar } from "react-bootstrap";

import packInfo from "../../package.json";

function MainNavbar() {
  return (
    <Navbar className="bg-success navbar navbar-expand-lg fixed-top navbar-dark">
      <Container>
        <Navbar.Brand href="#" className="headelem">
          SyncStar
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>v{packInfo.version}</Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default MainNavbar;
