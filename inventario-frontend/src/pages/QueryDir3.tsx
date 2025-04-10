import {withAuthenticationRequired} from "react-oidc-context";
import React, {useEffect} from "react";
import {Button, Col, Form, InputGroup} from "react-bootstrap";
import useUnidadesDir3 from "../common/useUnidadesDir3";
import useUnidadDir3 from "../common/useUnidadDir3";
import ResultList from "./ResultList";
import './QueryDir3.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

type Props = {
    codigo_unidad?: string,
    label?: string;
    onChange?: (codigoDir3: string | undefined) => void
};

const QueryDir3 = (props: Props) => {
    const [searchTerm, setSearchTerm] = React.useState('');
    const [activeIndex, setActiveIndex] = React.useState(-1);
    const [selected, setSelected] = React.useState<boolean>(false);
    const [codigoSeleccionado, setCodigoSeleccionado] = React.useState<string | undefined>(undefined);

    const {unidadesDir3, loading} = useUnidadesDir3(searchTerm);
    const {unidadDir3} = useUnidadDir3(props.codigo_unidad);

    const inputRef = React.createRef<HTMLInputElement>();

    const handleSelect = (codigoDir3: string) => {
        setCodigoSeleccionado(codigoDir3);
        if (props.onChange) {
            props.onChange(codigoDir3)
        }
        const name = unidadesDir3.find(u => u.unidad_id === codigoDir3)?.nombre;
        setSearchTerm(name || ``)
        setActiveIndex(-1)
        setSelected(true)
    };

    useEffect(() => {
        setCodigoSeleccionado(unidadDir3?.unidad_id);
        setSearchTerm(unidadDir3?.nombre || '')
        setSelected(true)
    }, [unidadDir3]);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (selected) {
            setSelected(false)
            setCodigoSeleccionado(undefined)
        }
        setSearchTerm(event.target.value);
    };

    const onKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {

        if (event.key === "ArrowDown") {
            setActiveIndex((prev) => (prev + 1) % unidadesDir3.length);
        }
        if (event.key === "ArrowUp") {
            setActiveIndex((prev) => (prev - 1 + unidadesDir3.length) % unidadesDir3.length);
        }
        if (activeIndex !== -1 && event.key === "Enter") {
            handleSelect(unidadesDir3[activeIndex].unidad_id);
        }
    };

    const unidades = Object.assign({}, ...unidadesDir3?.map(s => ({[s.unidad_id]: s.nombre_unidad_padre + ' / ' + s.nombre})));

    function clearCodigoSeleccionado() {
        setCodigoSeleccionado(undefined);
        setSearchTerm("");
        inputRef.current?.focus()
    }

    return (
        <div>

            <Form.Label>{props.label || 'Código unidad'}</Form.Label>
            <InputGroup>
                <InputGroup.Text as={Col} md={2}>{codigoSeleccionado}</InputGroup.Text>
                <Form.Control type="text" onChange={handleChange}
                              onKeyDown={onKeyDown}
                              ref={inputRef}
                              autoComplete={"off"}
                              placeholder={"Introduzca el nombre de la unidad para buscar"}
                              value={searchTerm || ''}/>
                <Button variant={"light"} onClick={clearCodigoSeleccionado}><FontAwesomeIcon icon={"eraser"}/></Button>
            </InputGroup>
            {searchTerm && !selected ? (
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
                <></>
                // <div>Escriba para empezar a buscar</div>
            )}

        </div>
    )
}

export default withAuthenticationRequired(QueryDir3, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});