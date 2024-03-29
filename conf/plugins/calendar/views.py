import calendar
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect

from core import models
from core.decorator import cache_page
from core.utils.utils import create_crumbs

from .issue_calendar import IssueCalendar

from onisite.plugins.calendar import config

@cache_page(settings.DEFAULT_TTL_SECONDS)
def all_issues_calendar(request, year=None):
    # NE theme change
    page_title = "Calendar of Issues"
    # / NE theme change
    page_name = "issues"
    crumbs = list(settings.BASE_CRUMBS)
    display_multiple = config.MULTIPLES_ALL_ISSUES
    calendar = IssueCalendar(None, year)
    return render(request, 'all_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def title_issues_calendar(request, lccn, year=None):
    title = get_object_or_404(models.Title, lccn=lccn)
    page_title = "Browse Issues: %s" % title.display_name
    page_name = "issues_title"
    # always display where a single title has multiple issues on a day
    display_multiple = True
    crumbs = create_crumbs(title)
    calendar = IssueCalendar(title, year)
    return render(request, 'title_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def issues_for_date(request, lccn, year, month, day):
    m, d, y = int(month), int(day), int(year)
    datestring = "%s %d, %d" % (calendar.month_name[m], d, y)
    page_title = "Issues published on %s" % datestring
    dt = datetime.date(y, m, d)
    page_name = "issues_for_date"
    dtstr = "%04d-%02d-%02d" % (y, m, d)

    if lccn == "all":
        issues = models.Issue.objects.filter(date_issued = dt)

    else:
        title = get_object_or_404(models.Title, lccn=lccn)
        issues = models.Issue.objects.filter(date_issued = dt, title_id = lccn)
        page_title = title.name + ": " + page_title

        # For a single issue on a specific title, we just redirect the user to
        # the issue in our newspaper viewer
        if len(issues) == 1:
            issue = issues[0]
            return redirect("openoni_issue_pages", issue.title.lccn, dtstr, issue.edition)

    return render(request, 'issues_for_date.html', locals())
