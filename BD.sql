USE [SIAC]
GO

/****** Object:  Table [dbo].[S17Web_LIC_CiiuRiesgo]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_CiiuRiesgo](
	[idCiiuRiesgo] [int] IDENTITY(1,1) NOT NULL,
	[codigoCiiu] [char](6) NULL,
	[fkPreCalificacion] [int] NOT NULL,
	[estado] [char](1) NOT NULL,
	[RecordCreateDate] [datetime] NOT NULL,
	[RecordCreateUser] [varchar](100) NOT NULL,
	[RecordState] [varchar](1) NOT NULL,
	[C_GiroNeg] [char](6) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idCiiuRiesgo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Cuestionario]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Cuestionario](
	[idCuestionario] [int] IDENTITY(1,1) NOT NULL,
	[fkPreCalificacion] [int] NOT NULL,
	[fkpregunta] [int] NOT NULL,
	[pregunta] [varchar](200) NOT NULL,
	[respuesta] [char](100) NOT NULL,
	[estado] [char](1) NOT NULL,
	[RecordCreateDate] [datetime] NOT NULL,
	[RecordCreateUser] [varchar](100) NOT NULL,
	[RecordState] [varchar](1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idCuestionario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Documentacion]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Documentacion](
	[C_Documentac] [int] IDENTITY(1,1) NOT NULL,
	[C_Evaluacion] [int] NOT NULL,
	[C_TipoDocum] [int] NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_Documentacion] PRIMARY KEY CLUSTERED 
(
	[C_Documentac] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Evaluacion]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Evaluacion](
	[C_Evaluacion] [int] IDENTITY(1,1) NOT NULL,
	[idPreCalificacion] [int] NOT NULL,
	[C_TipEval] [tinyint] NOT NULL,
	[T_Eval_Coment] [varchar](max) NOT NULL,
	[C_Usuari_Login] [char](20) NOT NULL,
	[D_Usuari_FecDig] [smalldatetime] NOT NULL,
	[N_Usuari_PC] [varchar](20) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_Evaluacion] PRIMARY KEY CLUSTERED 
(
	[C_Evaluacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_EvalUsu]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_EvalUsu](
	[C_EvalUsu] [int] IDENTITY(1,1) NOT NULL,
	[C_TipEval] [tinyint] NOT NULL,
	[C_Usuari_Login] [char](20) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_EvalUsu] PRIMARY KEY CLUSTERED 
(
	[C_EvalUsu] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Firma_Archivo]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Firma_Archivo](
	[C_FileFirma] [int] IDENTITY(1,1) NOT NULL,
	[idRequisitoArchivo] [int] NOT NULL,
	[C_FileFirma_Ord] [int] NOT NULL,
	[N_FileFirma_Nombre] [varchar](100) NOT NULL,
	[N_FileFirma_Ruta] [varchar](150) NOT NULL,
	[C_Usuari_Login] [char](20) NOT NULL,
	[D_FileFirma_FecDig] [smalldatetime] NOT NULL,
	[F_FileFirma_Estado] [char](1) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_Firma_Archivo] PRIMARY KEY CLUSTERED 
(
	[C_FileFirma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [IX_S17Web_LIC_Firma_Archivo] UNIQUE NONCLUSTERED 
(
	[idRequisitoArchivo] ASC,
	[C_FileFirma_Ord] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_PreCalificacion]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_PreCalificacion](
	[idPreCalificacion] [int] IDENTITY(1,1) NOT NULL,
	[fkContribuyente] [char](11) NOT NULL,
	[codigoCatastral] [char](11) NOT NULL,
	[direccionCatastral] [varchar](300) NOT NULL,
	[areaNegocio] [decimal](18, 4) NOT NULL,
	[fkRiesgo] [int] NOT NULL,
	[fkRiesgoEvaluado] [int] NOT NULL,
	[fkFuncion] [int] NOT NULL,
	[fkCompatibilidadCU] [int] NOT NULL,
	[fkCompatibilidadDL] [int] NOT NULL,
	[monto] [decimal](12, 2) NOT NULL,
	[estado] [char](1) NOT NULL,
	[observacion] [text] NOT NULL,
	[RecordCreateDate] [datetime] NOT NULL,
	[RecordCreateUser] [varchar](100) NOT NULL,
	[RecordState] [varchar](1) NOT NULL,
	[idContribuyente] [int] NOT NULL,
	[descripcion] [text] NOT NULL,
	[correo] [varchar](150) NOT NULL,
	[telefono] [varchar](15) NOT NULL,
	[C_TipLic] [char](1) NULL,
	[C_TipTra] [char](8) NULL,
	[F_TipTra_Origen] [char](1) NULL,
	[C_TipTra_Anio] [char](4) NULL,
	[idUsuarioContribuyente] [int] NOT NULL,
	[nombreComercial] [text] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idPreCalificacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Requisito_Archivo]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Requisito_Archivo](
	[idRequisitoArchivo] [int] IDENTITY(1,1) NOT NULL,
	[fkPreCalificacion] [int] NOT NULL,
	[anexo] [varchar](300) NOT NULL,
	[idRequisito] [char](2) NOT NULL,
	[ruta] [varchar](150) NOT NULL,
	[numeroFolio] [int] NOT NULL,
	[enlace] [text] NOT NULL,
	[observacion] [varchar](300) NOT NULL,
	[RecordCreateDate] [datetime] NOT NULL,
	[RecordCreateUser] [varchar](100) NOT NULL,
	[RecordState] [char](1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idRequisitoArchivo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_Sectores]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_Sectores](
	[C_Sector] [int] IDENTITY(1,1) NOT NULL,
	[N_Sector] [varchar](50) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_Sectores] PRIMARY KEY CLUSTERED 
(
	[C_Sector] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_TipoDocum]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_TipoDocum](
	[C_TipoDocum] [int] IDENTITY(1,1) NOT NULL,
	[C_Sector] [int] NOT NULL,
	[N_TipoDocum] [varchar](400) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_TipoDocum] PRIMARY KEY CLUSTERED 
(
	[C_TipoDocum] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_TipoEval]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_TipoEval](
	[C_TipEval] [tinyint] IDENTITY(1,1) NOT NULL,
	[N_TipEval] [varchar](50) NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_TipoEval] PRIMARY KEY CLUSTERED 
(
	[C_TipEval] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[S17Web_LIC_VBExpediente]    Script Date: 27/04/2022 09:12:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[S17Web_LIC_VBExpediente](
	[C_VBExp] [int] IDENTITY(1,1) NOT NULL,
	[idPreCalificacion] [int] NOT NULL,
	[C_TipEval] [tinyint] NOT NULL,
	[F_VBExp_Eval] [char](1) NOT NULL,
	[T_VBExp_Obs] [varchar](400) NOT NULL,
	[C_Usuari_Login] [char](20) NOT NULL,
	[F_VBExp_FecDig] [smalldatetime] NOT NULL,
 CONSTRAINT [PK_S17Web_LIC_VBExpediente] PRIMARY KEY CLUSTERED 
(
	[C_VBExp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [IX_S17Web_LIC_VBExpediente] UNIQUE NONCLUSTERED 
(
	[idPreCalificacion] ASC,
	[C_TipEval] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo] ADD  DEFAULT ('1') FOR [estado]
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo] ADD  DEFAULT ('') FOR [RecordCreateUser]
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo] ADD  DEFAULT ('1') FOR [RecordState]
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo] ADD  DEFAULT ('') FOR [C_GiroNeg]
GO

ALTER TABLE [dbo].[S17Web_LIC_Cuestionario] ADD  DEFAULT ('1') FOR [estado]
GO

ALTER TABLE [dbo].[S17Web_LIC_Cuestionario] ADD  DEFAULT ('') FOR [RecordCreateUser]
GO

ALTER TABLE [dbo].[S17Web_LIC_Cuestionario] ADD  DEFAULT ('1') FOR [RecordState]
GO

ALTER TABLE [dbo].[S17Web_LIC_Firma_Archivo] ADD  CONSTRAINT [DF_S17Web_LIC_Firma_Archivo_F_Estado]  DEFAULT ((1)) FOR [F_FileFirma_Estado]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('1') FOR [estado]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('') FOR [RecordCreateUser]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('1') FOR [RecordState]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ((1)) FOR [idContribuyente]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('') FOR [descripcion]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('') FOR [correo]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('') FOR [telefono]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ((1)) FOR [idUsuarioContribuyente]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] ADD  DEFAULT ('') FOR [nombreComercial]
GO

ALTER TABLE [dbo].[S17Web_LIC_Requisito_Archivo] ADD  DEFAULT ('') FOR [RecordCreateUser]
GO

ALTER TABLE [dbo].[S17Web_LIC_Requisito_Archivo] ADD  DEFAULT ('1') FOR [RecordState]
GO

ALTER TABLE [dbo].[S17Web_LIC_TipoDocum] ADD  CONSTRAINT [DF_S17Web_LIC_TipoDocum_C_Sector]  DEFAULT ((1)) FOR [C_Sector]
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_CiiuRiesgo_S17Web_LIC_PreCalificacion] FOREIGN KEY([fkPreCalificacion])
REFERENCES [dbo].[S17Web_LIC_PreCalificacion] ([idPreCalificacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_CiiuRiesgo] CHECK CONSTRAINT [FK_S17Web_LIC_CiiuRiesgo_S17Web_LIC_PreCalificacion]
GO

ALTER TABLE [dbo].[S17Web_LIC_Cuestionario]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Cuestionario_S17Web_LIC_PreCalificacion] FOREIGN KEY([fkPreCalificacion])
REFERENCES [dbo].[S17Web_LIC_PreCalificacion] ([idPreCalificacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_Cuestionario] CHECK CONSTRAINT [FK_S17Web_LIC_Cuestionario_S17Web_LIC_PreCalificacion]
GO

ALTER TABLE [dbo].[S17Web_LIC_Documentacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Documentacion_S17Web_LIC_Evaluacion] FOREIGN KEY([C_Evaluacion])
REFERENCES [dbo].[S17Web_LIC_Evaluacion] ([C_Evaluacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_Documentacion] CHECK CONSTRAINT [FK_S17Web_LIC_Documentacion_S17Web_LIC_Evaluacion]
GO

ALTER TABLE [dbo].[S17Web_LIC_Documentacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Documentacion_S17Web_LIC_TipoDocum] FOREIGN KEY([C_TipoDocum])
REFERENCES [dbo].[S17Web_LIC_TipoDocum] ([C_TipoDocum])
GO

ALTER TABLE [dbo].[S17Web_LIC_Documentacion] CHECK CONSTRAINT [FK_S17Web_LIC_Documentacion_S17Web_LIC_TipoDocum]
GO

ALTER TABLE [dbo].[S17Web_LIC_Evaluacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Evaluacion_S17Web_LIC_PreCalificacion] FOREIGN KEY([idPreCalificacion])
REFERENCES [dbo].[S17Web_LIC_PreCalificacion] ([idPreCalificacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_Evaluacion] CHECK CONSTRAINT [FK_S17Web_LIC_Evaluacion_S17Web_LIC_PreCalificacion]
GO

ALTER TABLE [dbo].[S17Web_LIC_Evaluacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Evaluacion_S17Web_LIC_TipoEval] FOREIGN KEY([C_TipEval])
REFERENCES [dbo].[S17Web_LIC_TipoEval] ([C_TipEval])
GO

ALTER TABLE [dbo].[S17Web_LIC_Evaluacion] CHECK CONSTRAINT [FK_S17Web_LIC_Evaluacion_S17Web_LIC_TipoEval]
GO

ALTER TABLE [dbo].[S17Web_LIC_Firma_Archivo]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Firma_Archivo_S17Web_LIC_Requisito_Archivo] FOREIGN KEY([idRequisitoArchivo])
REFERENCES [dbo].[S17Web_LIC_Requisito_Archivo] ([idRequisitoArchivo])
GO

ALTER TABLE [dbo].[S17Web_LIC_Firma_Archivo] CHECK CONSTRAINT [FK_S17Web_LIC_Firma_Archivo_S17Web_LIC_Requisito_Archivo]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_PreCalificacion_S17Web_Contribuyente] FOREIGN KEY([idContribuyente])
REFERENCES [dbo].[s17Web_Contribuyente] ([IdContribuyente])
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] CHECK CONSTRAINT [FK_S17Web_LIC_PreCalificacion_S17Web_Contribuyente]
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_PreCalificacion_S17Web_UsuarioContribuyente] FOREIGN KEY([idUsuarioContribuyente])
REFERENCES [dbo].[S17Web_UsuarioContribuyente] ([id])
GO

ALTER TABLE [dbo].[S17Web_LIC_PreCalificacion] CHECK CONSTRAINT [FK_S17Web_LIC_PreCalificacion_S17Web_UsuarioContribuyente]
GO

ALTER TABLE [dbo].[S17Web_LIC_Requisito_Archivo]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_Requisito_Archivo_S17Web_LIC_PreCalificacion] FOREIGN KEY([fkPreCalificacion])
REFERENCES [dbo].[S17Web_LIC_PreCalificacion] ([idPreCalificacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_Requisito_Archivo] CHECK CONSTRAINT [FK_S17Web_LIC_Requisito_Archivo_S17Web_LIC_PreCalificacion]
GO

ALTER TABLE [dbo].[S17Web_LIC_VBExpediente]  WITH CHECK ADD  CONSTRAINT [FK_S17Web_LIC_VBExpediente_S17Web_LIC_PreCalificacion] FOREIGN KEY([idPreCalificacion])
REFERENCES [dbo].[S17Web_LIC_PreCalificacion] ([idPreCalificacion])
GO

ALTER TABLE [dbo].[S17Web_LIC_VBExpediente] CHECK CONSTRAINT [FK_S17Web_LIC_VBExpediente_S17Web_LIC_PreCalificacion]
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Estado del archivo 1 = activo, 2 = eliminado' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'S17Web_LIC_Firma_Archivo', @level2type=N'COLUMN',@level2name=N'F_FileFirma_Estado'
GO


USE [SIAC]
GO

/****** Object:  View [dbo].[Usuarios]    Script Date: 27/04/2022 09:12:40 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE VIEW [dbo].[Usuarios]
AS
SELECT C_Usuari_Login,
CONVERT(varchar(255), NEWID()) as N_Usuari_Clave,
N_Usuari_Nombre,
F_Usuari_Activo,
F_Usuari_Admin,
D_Usuari_FecIni,
D_Usuari_FecFin,
C_Usuari_Resp,
D_Usuari_FecDig,
C_Usucodi,
C_UsuCold,
F_Usuari_SNP,
M_Usuari_DNI,
N_Usuari_RespPC,
F_Usuari_Fiscal,
N_Usuari_claveSGAD,
last_login,
F_Usuari_Admin as is_superuser
FROM GENERAL.DBO.Usuarios 
GO


USE [SIAC]
GO

/****** Object:  StoredProcedure [dbo].[S17Web_LIC_BuscarRequisitoArchivo]    Script Date: 27/04/2022 09:13:23 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script para el comando SelectTopNRows de SSMS  ******/
CREATE PROCEDURE [dbo].[S17Web_LIC_BuscarRequisitoArchivo]
@Opcion char(2),
@Valor01 varchar(50)
AS


IF @Opcion  = '01'
BEGIN
	declare @idPreCalificacion int = convert(int, @Valor01)
	

	SELECT S17Web_LIC_PreCalificacion.idPreCalificacion,
	S17Web_LIC_PreCalificacion.C_TipLic,
	S17Web_LIC_PreCalificacion.C_TipTra,
	S17Web_LIC_PreCalificacion.F_TipTra_Origen,
	S17Web_LIC_PreCalificacion.C_TipTra_Anio,
	S01TipoTramite.N_TipTra_Nombre,
	S01Reqtupa.N_ReqTup_Item,
	S01Reqtupa.N_ReqTup_descrip,
	S17Web_LIC_Requisito_Archivo.idRequisitoArchivo,
	S17Web_LIC_Requisito_Archivo.fkPreCalificacion,
	S17Web_LIC_Requisito_Archivo.anexo,
	S17Web_LIC_Requisito_Archivo.idRequisito,
	S17Web_LIC_Requisito_Archivo.ruta,
	S17Web_LIC_Requisito_Archivo.numeroFolio,
	S17Web_LIC_Requisito_Archivo.enlace,
	S17Web_LIC_Requisito_Archivo.observacion,
	S17Web_LIC_Requisito_Archivo.RecordCreateDate,
	S17Web_LIC_Requisito_Archivo.RecordCreateUser,
	S17Web_LIC_Requisito_Archivo.RecordState,
	TFirmaArchivo.C_FileFirma,
	TFirmaArchivo.C_FileFirma_Ord,
	TFirmaArchivo.N_FileFirma_Nombre,
	TFirmaArchivo.N_FileFirma_Ruta,
	TFirmaArchivo.C_Usuari_Login,
	TFirmaArchivo.D_FileFirma_FecDig,
	TFirmaArchivo.F_FileFirma_Estado
	FROM S17Web_LIC_PreCalificacion 
	INNER JOIN S01TipoTramite
	ON S17Web_LIC_PreCalificacion.C_TipTra = S01TipoTramite.C_TipTra
	AND S17Web_LIC_PreCalificacion.C_TipTra_Anio = S01TipoTramite.C_TipTra_Anio 
	AND S17Web_LIC_PreCalificacion.F_TipTra_Origen = S01TipoTramite.F_TipTra_Origen 
	INNER JOIN S01Reqtupa
	ON S01TipoTramite.C_TipTra = S01Reqtupa.C_TipTra
	AND S01TipoTramite.C_TipTra_Anio = S01Reqtupa.C_TipTra_Anio 
	AND S01TipoTramite.F_TipTra_Origen = S01Reqtupa.F_TipTra_Origen
	LEFT JOIN S17Web_LIC_Requisito_Archivo
	ON S17Web_LIC_PreCalificacion.idPreCalificacion = S17Web_LIC_Requisito_Archivo.[fkPreCalificacion]
	AND S01Reqtupa.N_ReqTup_Item = S17Web_LIC_Requisito_Archivo.idRequisito
	LEFT JOIN (SELECT S17Web_LIC_Firma_Archivo.C_FileFirma,
		S17Web_LIC_Firma_Archivo.idRequisitoArchivo,
		S17Web_LIC_Firma_Archivo.C_FileFirma_Ord,
		S17Web_LIC_Firma_Archivo.N_FileFirma_Nombre,
		S17Web_LIC_Firma_Archivo.N_FileFirma_Ruta,
		S17Web_LIC_Firma_Archivo.C_Usuari_Login,
		S17Web_LIC_Firma_Archivo.D_FileFirma_FecDig,
		S17Web_LIC_Firma_Archivo.F_FileFirma_Estado
		FROM	(SELECT idRequisitoArchivo, MAX(C_FileFirma_Ord) AS C_FileFirma_Ord
				FROM S17Web_LIC_Firma_Archivo
				WHERE F_FileFirma_Estado = 1
				GROUP BY idRequisitoArchivo) AS TUltReqArchivo
		INNER JOIN S17Web_LIC_Firma_Archivo
		ON TUltReqArchivo.idRequisitoArchivo = S17Web_LIC_Firma_Archivo.idRequisitoArchivo
		AND TUltReqArchivo.C_FileFirma_Ord = S17Web_LIC_Firma_Archivo.C_FileFirma_Ord) AS TFirmaArchivo
	ON S17Web_LIC_Requisito_Archivo.idRequisitoArchivo = TFirmaArchivo.idRequisitoArchivo
	WHERE S17Web_LIC_PreCalificacion.idPreCalificacion = @idPreCalificacion  
	ORDER BY S01Reqtupa.N_ReqTup_Item
END

GO


