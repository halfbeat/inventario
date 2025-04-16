import {Breadcrumb, Nav} from "react-bootstrap";
import {Link, useLocation, useParams, useRoutes} from "react-router-dom";
import React from "react";

export const SistemaHeader = () => {
    let params = useParams();
    let location = useLocation();

    return (
        <>
            <Breadcrumb>
                <Breadcrumb.Item linkAs={Link} linkProps={{to: "/home"}}>Inicio</Breadcrumb.Item>
                <Breadcrumb.Item linkAs={Link} linkProps={{to: "/sistemas"}}> Sistemas </Breadcrumb.Item>
                <Breadcrumb.Item active>{params.sistema_id}</Breadcrumb.Item>
            </Breadcrumb>
            <p className={"h4 border border-2 rounded p-2"}>Sistema {params.sistema_id}</p>

            <Nav variant="tabs" className="mb-2">
                <Nav.Item>
                    <Nav.Link as={Link} active={location.pathname == `/sistemas/${params.sistema_id}`}
                              to={`/sistemas/${params.sistema_id}`}>General</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link as={Link} active={location.pathname == `/sistemas/${params.sistema_id}/componentes`}
                              to={`/sistemas/${params.sistema_id}/componentes`}>Componentes</Nav.Link>
                </Nav.Item>
            </Nav>
        </>
    )
}