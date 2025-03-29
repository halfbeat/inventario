import {withAuthenticationRequired} from "react-oidc-context";
import React from "react";
import {Col, Form, InputGroup, Row} from "react-bootstrap";
import useUnidadesDir3 from "../common/useUnidadesDir3";
import ResultList from "./ResultList";
import './QueryDir3.css'

const QueryDir3 = () => {
    const [searchTerm, setSearchTerm] = React.useState('');
    const [activeIndex, setActiveIndex] = React.useState(-1);

    const {unidadesDir3, loading} = useUnidadesDir3(
        searchTerm
    );

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(event.target.value);
    };

    const handleSelect = (nombreUnidad: string) => {
        console.log(activeIndex, nombreUnidad);
        setSearchTerm(nombreUnidad);
    };

    const handleChangeNombre = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(event.target.value);
    };

    const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {

        if (event.key === "ArrowDown") {
            setActiveIndex((prev) => (prev + 1) % unidadesDir3.length);
        }
        if (event.key === "ArrowUp") {
            setActiveIndex((prev) => (prev - 1 + unidadesDir3.length) % unidadesDir3.length);
        }
        if (event.key === "Enter") {
            setSearchTerm(unidadesDir3[activeIndex].nombre);
        }
    };

    const unidades = Object.assign({}, ...unidadesDir3?.map(s => ({[s.unidad_id]: s.nombre_unidad_padre + '/' + s.nombre})));
    return (
        <Form>
            <InputGroup as={Row}>
                <InputGroup.Text as={Col} md={2}>[CODIGO]</InputGroup.Text>
                <Form.Control type="text" onChange={handleChangeNombre}
                              onKeyDown={onKeyDown}
                              autoComplete={"off"}
                              value={searchTerm || ''}/>
            </InputGroup>
            <Row>
                <Form.Group as={Col} md={2} controlId="codigoDir3">
                    <Form.Label>Código unidad</Form.Label>
                    <Form.Control type="text" disabled/>
                </Form.Group>
                <Form.Group as={Col} md={10} controlId="nombre">
                    <Form.Label>Nombre unidad</Form.Label>

                </Form.Group>
            </Row>
            <div className={"my-4 p-2 border"}>
                {searchTerm ? (
                    <div className={"result-container"}>
                        <ResultList
                            results={unidades}
                            searchTerm={searchTerm}
                            loading={loading}
                            handleSelect={handleSelect}
                            activeIndex={activeIndex}
                        />
                    </div>
                ) : (
                    <div>Start typing to search</div>
                )}
            </div>
        </Form>
    )
}

export default withAuthenticationRequired(QueryDir3, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});