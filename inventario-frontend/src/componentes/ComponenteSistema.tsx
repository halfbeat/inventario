import {Button, Card, Col, Form, Row} from "react-bootstrap";
import {Editor} from "@tinymce/tinymce-react";
import React, {useEffect, useRef, useState} from "react";
import {ComponenteSistemaDto, TipoComponenteDto} from "../openapi/api";
import {Editor as TinyMCEEditor} from "tinymce";
import {SubmitHandler, useForm} from "react-hook-form";
import useApi from "../common/useApi";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

interface ComponenteSistemaProps {
    sistemaId?: string | undefined
    componenteId?: string | undefined
}

type FormProps = {
    componente_id: string | undefined,
    nombre: string,
    tipo: string,
    gitUrl: string | undefined,
    observaciones: string | undefined,
}

export const ComponenteSistema = ({sistemaId, componenteId}: ComponenteSistemaProps) => {
    const api = useApi();
    const [componente, setComponente] = useState<ComponenteSistemaDto | null>(null);
    const editorRef = useRef<TinyMCEEditor | null>(null);
    const {
        register,
        handleSubmit,
        setValue,
        formState: {errors},
    } = useForm<FormProps>()

    useEffect(() => {
        if (sistemaId && componenteId && api) {
            api.sistemas.getComponenteSistemaInformacion(sistemaId, componenteId)
                .then(res => res.data)
                .then(data => {
                    setComponente(data);
                    setValue("componente_id", data.componente_id)
                    setValue('nombre', data.nombre);
                    setValue("tipo", data.tipo)
                    setValue("gitUrl", data.git_repo)
                    setValue("observaciones", data.observaciones)
                    editorRef.current?.setContent(data.observaciones || '')
                })
                .catch(err => console.error(err));
        }
    }, [sistemaId, componenteId, api]);

    const [tiposComponente, setTiposComponente] = useState<Array<TipoComponenteDto>>([]);
    useEffect(() => {
        function obtenerTiposComponente() {
            if (api) {
                api.tiposComponente.getTiposComponente()
                    .then(res => res.data)
                    .then(data => {
                        setTiposComponente(data);
                    })
                    .catch(err => console.error(err));
            }
        }

        obtenerTiposComponente()
    }, [api]);

    const onSubmit: SubmitHandler<FormProps> = (data) => {
        data.observaciones = editorRef.current?.getContent()
        const componenteDtp = {
            sistema_id: sistemaId,
            componente_id: data.componente_id,
            nombre: data.nombre,
            tipo: data.tipo,
            git_repo: data.gitUrl,
            observaciones: data.observaciones,
        } as ComponenteSistemaDto;
        if (api && sistemaId && data.componente_id) {
            console.log(data.componente_id)
            api.sistemas.modificarComponenteSistemaInformacion(
                sistemaId, data.componente_id, componenteDtp
            )
                .catch(err => console.error(err));
        }
    }


    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="componente_id">
                    <Form.Label>Identificador</Form.Label>
                    <Form.Control disabled={componenteId != undefined} type="text"
                                  placeholder="Id. del componente"
                                  {...register("componente_id", {required: true, pattern: /^[A-Za-z0-9_-]+$/i})}
                                  aria-invalid={errors.componente_id ? "true" : "false"}/>
                    {errors.componente_id?.type === "required" && (
                        <span role="alert">El identificador es obligatorio</span>
                    )}
                    {errors.componente_id?.type === "pattern" && (
                        <span role="alert">El identificador no es válido. Solo se adminten letras, números y los caracteres - y _</span>
                    )}
                </Form.Group>
            </Row>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="nombre">
                    <Form.Label>Nombre</Form.Label>
                    <Form.Control type="text" placeholder="Nombre del componente"
                                  {...register("nombre", {required: true, maxLength: 50})}/>
                    {errors.nombre?.type === "required" && (
                        <span role="alert">El nombre es obligatorio</span>
                    )}
                    {errors.nombre?.type === "maxLength" && (
                        <span role="alert">El nombre no puede tener una longitud superior a 50 caracteres</span>
                    )}
                </Form.Group>
            </Row>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="tipo">
                    <Form.Label>Tipo</Form.Label>
                    <Form.Select
                        {...register("tipo", {required: true})} >
                        <option value="">Seleccione un tipo</option>
                        {tiposComponente.map(tipo => (
                            <option key={tipo.tipo} value={tipo.tipo}>{tipo.nombre}</option>
                        ))}
                    </Form.Select>
                    {errors.tipo?.type === "required" && (
                        <span role="alert">El tipo es obligatorio</span>
                    )}
                </Form.Group>
            </Row>
            <Row className="mb-3">
                <Form.Group as={Col} controlId="git-url">
                    <Form.Label>Repositorio Git</Form.Label>
                    <Form.Control type="text"
                                  placeholder="Dirección http del repositorio Git" {...register("gitUrl")}/>
                </Form.Group>
            </Row>
            <Row className="mb-3">
                <Form.Group as={Col} md={12} controlId="observaciones">
                    <Form.Label>Observaciones</Form.Label>

                    <Editor
                        tinymceScriptSrc={`${process.env.PUBLIC_URL}/tinymce/tinymce.min.js`}
                        onInit={(evt, editor) => editorRef.current = editor}
                        initialValue={componente?.observaciones}
                        init={{
                            height: 300,
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
                <Button type={"submit"} className={" "} variant={"primary"}>
                    <FontAwesomeIcon icon={"floppy-disk"}/> Grabar
                </Button>
            </div>
        </Form>
    )
}