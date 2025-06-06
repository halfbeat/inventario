/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface ErrorDto {
  codigo: string;
  descripcion: string;
  descripcionDetallada?: string;
}

export interface ListadoPaginadoResumenSistemasDto {
  total: number;
  page: number;
  page_size: number;
  items: ResumenSistemaInformacionDto[];
}

export interface ResumenSistemaInformacionDto {
  sistema_id: string;
  nombre: string;
  unidad_responsable?: string;
  tecnico_responsable?: string;
}

export interface SistemaInformacionDto {
  sistema_id: string;
  nombre: string;
  unidad_responsable?: string;
  tecnico_responsable?: string;
  observaciones?: string;
}

export interface UnidadDIR3Dto {
  unidad_id: string;
  unidad_padre_id?: string;
  nombre: string;
  nombre_unidad_padre?: string;
}

export interface ListadoPaginadoUnidadesDIR3Dto {
  total: number;
  page: number;
  page_size: number;
  items: UnidadDIR3Dto[];
}

export interface ComponenteSistemaDto {
  sistema_id: string;
  tipo: string;
  componente_id: string;
  nombre: string;
  git_repo?: string;
  observaciones?: string;
}

export interface TipoComponenteDto {
  tipo: string;
  nombre: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "https://jcweb24des101.ae.jcyl.es/{basePath}";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title Inventario de aplicaciones GSS
 * @version 1.0.0
 * @license MIT (https://opensource.org/licenses/MIT)
 * @termsOfService https://www.jcyl.es/terminosServicio
 * @baseUrl https://jcweb24des101.ae.jcyl.es/{basePath}
 * @contact <jesvizan@jcyl.es>
 *
 * Api REST del inventario de aplicaciones GSS
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  sistemas = {
    /**
     * No description
     *
     * @tags sistemas
     * @name GetSistemasInformacion
     * @summary Listado paginado de sistemas de informacón
     * @request GET:/sistemas
     * @response `200` `ListadoPaginadoResumenSistemasDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getSistemasInformacion: (
      query?: {
        page?: any;
        page_size?: any;
      },
      params: RequestParams = {},
    ) =>
      this.request<ListadoPaginadoResumenSistemasDto, ErrorDto>({
        path: `/sistemas`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name RegistrarSistemaInformacion
     * @summary Registro de un sistema de información
     * @request POST:/sistemas
     * @response `200` `SistemaInformacionDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    registrarSistemaInformacion: (data: SistemaInformacionDto, params: RequestParams = {}) =>
      this.request<SistemaInformacionDto, ErrorDto>({
        path: `/sistemas`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name GetSistemaInformacion
     * @summary Recuperar la información de un sistema
     * @request GET:/sistemas/{sistemaId}
     * @response `200` `SistemaInformacionDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getSistemaInformacion: (sistemaId: string, params: RequestParams = {}) =>
      this.request<SistemaInformacionDto, ErrorDto>({
        path: `/sistemas/${sistemaId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name UpdateSistemaInformacion
     * @summary Modificar la información de un sistema
     * @request PUT:/sistemas/{sistemaId}
     * @response `200` `SistemaInformacionDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    updateSistemaInformacion: (sistemaId: string, data: SistemaInformacionDto, params: RequestParams = {}) =>
      this.request<SistemaInformacionDto, ErrorDto>({
        path: `/sistemas/${sistemaId}`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name GetComponentesSistemaInformacion
     * @summary Recuperar los componentes de un sistema
     * @request GET:/sistemas/{sistemaId}/componentes
     * @response `200` `(ComponenteSistemaDto)[]` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getComponentesSistemaInformacion: (sistemaId: string, params: RequestParams = {}) =>
      this.request<ComponenteSistemaDto[], ErrorDto>({
        path: `/sistemas/${sistemaId}/componentes`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name GetComponenteSistemaInformacion
     * @summary Recuperar un componente del sistema
     * @request GET:/sistemas/{sistemaId}/componentes/{componenteId}
     * @response `200` `ComponenteSistemaDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getComponenteSistemaInformacion: (sistemaId: string, componenteId: string, params: RequestParams = {}) =>
      this.request<ComponenteSistemaDto, ErrorDto>({
        path: `/sistemas/${sistemaId}/componentes/${componenteId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags sistemas
     * @name ModificarComponenteSistemaInformacion
     * @summary Modificar un componente del sistema
     * @request PUT:/sistemas/{sistemaId}/componentes/{componenteId}
     * @response `200` `ComponenteSistemaDto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    modificarComponenteSistemaInformacion: (
      sistemaId: string,
      componenteId: string,
      data: ComponenteSistemaDto,
      params: RequestParams = {},
    ) =>
      this.request<ComponenteSistemaDto, ErrorDto>({
        path: `/sistemas/${sistemaId}/componentes/${componenteId}`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
  dir3 = {
    /**
     * No description
     *
     * @tags dir3
     * @name QueryUnidadesDir3
     * @summary consulta de unidades dir3
     * @request GET:/dir3/unidades
     * @response `200` `ListadoPaginadoUnidadesDIR3Dto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    queryUnidadesDir3: (
      query?: {
        nombre?: string;
        id?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ListadoPaginadoUnidadesDIR3Dto, ErrorDto>({
        path: `/dir3/unidades`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags dir3
     * @name GetUnidadDir3
     * @summary Recuperar unidad DIR3
     * @request GET:/dir3/unidades/{unidad_id}
     * @response `200` `UnidadDIR3Dto` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `404` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getUnidadDir3: (unidadId: string, params: RequestParams = {}) =>
      this.request<UnidadDIR3Dto, ErrorDto>({
        path: `/dir3/unidades/${unidadId}`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
  tiposComponente = {
    /**
     * No description
     *
     * @tags tiposComponente
     * @name GetTiposComponente
     * @summary Recuperar tipos de componentes
     * @request GET:/tiposComponente
     * @response `200` `(TipoComponenteDto)[]` Operación realizada con éxito
     * @response `401` `ErrorDto`
     * @response `403` `ErrorDto`
     * @response `404` `ErrorDto`
     * @response `default` `ErrorDto`
     */
    getTiposComponente: (params: RequestParams = {}) =>
      this.request<TipoComponenteDto[], ErrorDto>({
        path: `/tiposComponente`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
}
