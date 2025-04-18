import {useParams} from "react-router-dom";
import {withAuthenticationRequired} from "react-oidc-context";
import React, {useEffect, useRef, useState} from "react";
import {SistemaInformacionDto} from "../openapi/api";
import {Button, Col, Form, Row} from "react-bootstrap";
import {Editor} from '@tinymce/tinymce-react';
import {Editor as TinyMCEEditor} from 'tinymce';
import {SubmitHandler, useForm} from "react-hook-form";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import QueryDir3 from "./QueryDir3";
import useApi from "../common/useApi";
import {SistemaHeader} from "./SistemaHeader";

const EditorSistema = () => {
    let params = useParams();
    const api = useApi();
    const editorRef = useRef<TinyMCEEditor | null>(null);
    const [sistema, setSistema] = useState({} as SistemaInformacionDto);
    const [unidadResponsableFuncional, setUnidadResponsableFuncional] = useState<string | undefined>('');

    type FormProps = {
        id: string
        nombre: string,
        observaciones: string | undefined,
        unidad_responsable_funcional: string | undefined,
    }
    const {
        register,
        handleSubmit,
        setValue,
        // formState: {errors},
    } = useForm<FormProps>()

    useEffect(() => {
        if (params.sistema_id && api) {
            api.sistemas.getSistemaInformacion(params.sistema_id)
                .then(res => res.data)
                .then(data => {
                    setSistema(data);
                    editorRef.current?.setContent(data.observaciones || '')
                    setValue('id', data.sistema_id)
                    setValue('nombre', data.nombre)
                    setUnidadResponsableFuncional(data.unidad_responsable)
                    setValue('observaciones', data.observaciones)
                })
                .catch(err => console.error(err));
        }
    }, [api, params.sistema_id, setValue])

    const onSubmit: SubmitHandler<FormProps> = (data) => {
        data.observaciones = editorRef.current?.getContent()
        const sistemaDto = {
            sistema_id: data.id,
            nombre: data.nombre,
            unidad_responsable: unidadResponsableFuncional,
            observaciones: data.observaciones
        } as SistemaInformacionDto;
        if (api) {
            api.sistemas.updateSistemaInformacion(params.sistema_id as string, sistemaDto)
                .then(res => res.data)
                .then(data => {
                    setSistema(data);
                    setValue('id', data.sistema_id)
                    setValue('nombre', data.nombre)
                    setValue('observaciones', data.observaciones)
                    setUnidadResponsableFuncional(data.unidad_responsable)
                })
                .catch(err => alert(JSON.stringify(err)));
        }
    }

    function handleOnChange(codigoDir3: string | undefined): void {
        setUnidadResponsableFuncional(codigoDir3)
    }

    return (
        <>
            <SistemaHeader/>
            <p className={"h4 p-2"}>Información general</p>
            <Form onSubmit={handleSubmit(onSubmit)}>
                <Row className="mb-3">
                    <Form.Group as={Col} md={2} controlId="id">
                        <Form.Label>ID</Form.Label>
                        <Form.Control type="text" disabled placeholder="Id del sistema" {...register("id")}/>
                    </Form.Group>
                    <Form.Group as={Col} controlId="nombre">
                        <Form.Label>Nombre</Form.Label>
                        <Form.Control type="text" placeholder="Nombre del sistema" {...register("nombre")}/>
                    </Form.Group>
                </Row>
                <Row>
                    <QueryDir3 codigo_unidad={unidadResponsableFuncional} label={"Unidad responsable"}
                               onChange={handleOnChange}/>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} md={2} controlId="fecha_registro">
                        <Form.Label>F. Registro</Form.Label>
                        <Form.Control type="date" placeholder="Fecha de registro"/>
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} md={12} controlId="observaciones">
                        <Form.Label>Observaciones</Form.Label>

                        <Editor
                            tinymceScriptSrc={`${process.env.PUBLIC_URL}/tinymce/tinymce.min.js`}
                            onInit={(evt, editor) => editorRef.current = editor}
                            initialValue={sistema.observaciones}
                            init={{
                                height: 500,
                                menubar: false,
                                plugins: [
                                    // 'advlist autolink lists link image charmap print preview anchor',
                                    // 'searchreplace visualblocks code fullscreen',
                                    // 'insertdatetime media table paste code help wordcount'
                                ],
                                toolbar: 'undo redo | formatselect | ' +
                                    'bold italic backcolor | alignleft aligncenter ' +
                                    'alignright alignjustify | bullist numlist outdent indent | ' +
                                    'removeformat | help',
                                content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
                            }}
                        />
                    </Form.Group>
                </Row>
                <div className={"text-end mt-3"}>
                    <Button disabled={params.sistema_id != null && sistema.sistema_id == null} type={"submit"}
                            className={" "} variant={"primary"}>
                        <FontAwesomeIcon icon={"floppy-disk"}/> {params.sistema_id ? 'Modificar' : 'Registrar'}
                    </Button>
                </div>
            </Form>
        </>
    )
}

export default withAuthenticationRequired(EditorSistema, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});