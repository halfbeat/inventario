import {Alert} from "react-bootstrap";

export function UnauthorizedPage() {
    return (
        <Alert variant="warning">
            Usted tiene permisos para realizar la operación o no se encuentra autenticado.<br/>
            Utilice <Alert.Link href={"/"}>este enlace</Alert.Link> para volver a la página de inicio.
        </Alert>
    )
}