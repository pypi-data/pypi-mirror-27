package com.qordoba.reporting.controller

import com.qordoba.reporting.model.PreFlightReport
import com.qordoba.reporting.model.preflight.{PageName, Project}
import com.qordoba.reporting.model.serializer.xlsx.ProjectPreFlightReportXlsxSerializer
import play.api.libs.json.Json
import play.api.mvc.{Action, Controller}
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

/**
 * This report Helps PMs manage progress of the project to Completion.
 * Is used with Report #2 to manage the Project This report also used to manage what new strings have come into the Project.
 */
class ProjectPreFlight extends Controller {
  /**
   * API to return part for the report for FE in olayer
   * @param projectId
   * @param languageId
   * @return
   */
  def index(projectId: Long, languageId: Long) = Action.async { request =>
    val offset = request.getQueryString("offset").map(_.toLong).getOrElse(0L)
    val limit = request.getQueryString("limit").map(_.toLong).getOrElse(10L)

    //new PreFlightReport().get(projectId, languageId, offset, limit).map { pages: List[PreFlightPage] =>
    Future {
      Ok("")
    }.recover {
      case e: Throwable =>
        InternalServerError(
          Json.obj("errMessage" -> e.getMessage, "techDetails" -> "")
        )
    }
  }

  /*
  Generate TM was moved to kafka and reactive streams WOW WOW
  def generateTM(projectId: Long, languageId: Long) = Action.async { request =>
    new PreFlightReport().processTM(projectId, languageId)
    Future.successful(Ok(Json.obj(
      "result" -> "success", "message" -> "Process Started"
    )))
  }
  */

  def export(projectId: Long, languageId: Long) = Action.async { request =>
    new PreFlightReport().get(projectId, languageId, 0, 0).map { report =>
      val project = Project.getProject(projectId, languageId)
      val pageNames = PageName.getNames(projectId, languageId)
      val file = new ProjectPreFlightReportXlsxSerializer().export(project, pageNames, report)
      Ok.sendFile(
        content = file,
        fileName = _ => file.getName
      )
    }
  }
}