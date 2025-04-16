import React, {useEffect, useState} from "react";
import useApi from "../common/useApi";
import {ComponenteSistemaDto} from "../openapi/api";
import {Table} from "react-bootstrap";
import "./ComponentesSistema.scss"
import {ComponenteSistema} from "./ComponenteSistema";

interface ComponentesSistemaProps {
    sistemaId?: string | undefined
}


export const ComponentesSistema = ({sistemaId}: ComponentesSistemaProps) => {
    const api = useApi();
    const [componentes, setComponentes] = useState([] as Array<ComponenteSistemaDto>);
    const [componenteId, setComponenteId] = useState<string | null>(null);

    const [selectedKey, setSelectedKey] = useState<string | null>(null);

    useEffect(() => {
        if (sistemaId && api) {
            api.sistemas.getComponentesSistemaInformacion(sistemaId)
                .then(res => res.data)
                .then(data => {
                    setComponentes(data);
                })
                .catch(err => console.error(err));
        }
    }, [api, sistemaId, setComponentes]);


    function selectComponente(componente_id: string) {
        setComponenteId(componente_id);
        setSelectedKey(componente_id);
    }


    return (
        <>
            <Table bordered>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Nombre</th>
                </tr>
                </thead>
                <tbody>
                {componentes?.map(s =>
                    <tr style={{cursor: "pointer"}} key={s.componente_id}
                        onClick={() => selectComponente(s.componente_id)}>
                        <td className={selectedKey === s.componente_id ? 'selected' : ''}> {s.componente_id}</td>
                        <td className={selectedKey === s.componente_id ? 'selected' : ''}>{s.nombre}</td>
                    </tr>)}
                </tbody>
            </Table>
            <p hidden={componenteId != undefined} className="text-light-emphasis">Seleccione un componente para
                editarlo</p>
            <ComponenteSistema sistemaId={sistemaId} componenteId={componenteId}/>
        </>
    )
}
