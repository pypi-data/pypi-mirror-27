<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet id='isystemTestReportXslt'
                version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Ignore this node when this file is embedded into xml report. -->
  <xsl:template match="xsl:stylesheet"/>
    
  <xsl:output method="html"
              encoding="utf-8"
              doctype-system="about:legacy-compat"/>

  <xsl:variable name="barGraphW">200</xsl:variable>
  <xsl:variable name="_okBkgColor" select="'#00ff00'"/>
  <xsl:variable name="_failBkgColor" select="'#ff8080'"/>
  <xsl:variable name="_errorBkgColor" select="'#c00000'"/>
  <xsl:variable name="_warnBkgColor" select="'#ff9422'"/>

  <xsl:variable name="_neutralBarBkgColor">#1e7ee0</xsl:variable>

  <xsl:variable name="_cvrgBarGraphW">150</xsl:variable>
  
  <xsl:template match="/">
    <!-- xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text -->
    <html>
      <head>
        <xsl:variable name="isEmbeddedXsltAndCss"
                      select='/reportDoc/main/reportConfig/isEmbeddedXsltCss'/>
          <xsl:choose>
              <xsl:when test="$isEmbeddedXsltAndCss = 'true'">
                  <link rel="stylesheet" type="text/css" href="#isystemTestReport.css"/>
              </xsl:when>
              <xsl:otherwise>
                  <xsl:variable name="href"
                                select='/reportDoc/main/reportConfig/cssFile'/>
                  <xsl:variable name="hrefWOBuiltIn"
                                select = "substring-after($href, '&lt;built-in&gt; ')"/>
                  <xsl:choose>
                    <xsl:when test="$hrefWOBuiltIn = ''">
                      <!-- there was no <built-in> prefix in report css tag -->  
                      <link rel="stylesheet" type="text/css" href="{$href}"/>
                    </xsl:when>
                    <xsl:otherwise>
                      <!-- there was <built-in> prefix in report css tag -->  
                      <link rel="stylesheet" type="text/css" href="{$hrefWOBuiltIn}"/>
                    </xsl:otherwise>
                  </xsl:choose>
              </xsl:otherwise>
          </xsl:choose>
      </head>
      <body>

        <xsl:call-template name="headerWithLogo"/>
        <p/>&#160;

        <xsl:apply-templates select="reportDoc/main/reportConfig"/>
        <p/>&#160;
        
        <xsl:apply-templates select="reportDoc/main/reportStatistic"/>
        <p/>&#160;

        <xsl:call-template name="testCasesWithFailuresAndErrors"/>
        
        <p/>&#160; <hr/> <p/>&#160;

        <xsl:call-template name="groupResultsTables"/>
        
        <p/>&#160; <hr/> <p/>&#160;

        <xsl:call-template name="testCaseResultsTables"/>
        
      </body>
    </html>
  </xsl:template>

  
  <xsl:template name="headerWithLogo">
      <table width='100%'>
          <tr>
              <td width='1%'>
                  <xsl:variable name="logoFile" select='/reportDoc/main/reportConfig/xmlLogoImage'/>
                  <img src="{$logoFile}"/>
              </td>
              <td>
                  <!-- When saxon will be used as processor, simplify this block to:
                       <xsl:value-of select="/reportDoc/main/reportConfig/xmlReportHeader"
                       disable-output-escaping="yes"/>
                  -->
                  <xsl:variable name="reportHdr" select="/reportDoc/main/reportConfig/xmlReportHeader"/>
                  <xsl:choose>
                      <xsl:when test="substring($reportHdr,1,1) = '&lt;'">
                          <!-- disable-output-escaping unfortunately does not work in Firefox! -->
                          <xsl:value-of select="$reportHdr"
                                        disable-output-escaping="yes"/>
                      </xsl:when>
                      <xsl:otherwise>
                          <h1 align="center">
                              <xsl:value-of select="$reportHdr"
                                            disable-output-escaping="yes"/>
                          </h1>
                      </xsl:otherwise>
                  </xsl:choose>
              </td>
          </tr>
      </table>
  </xsl:template>

  
<xsl:template match="tests">

      <tr>
        <th class="headerRow" colspan="3">Test Specification</th>
      </tr>
      
      <tr>
        <td colspan="3"><pre><xsl:value-of select='.'/></pre></td>
      </tr>

</xsl:template>


<xsl:template match="reportDoc/main/reportConfig">

    <table width = '100%'>
      <tr>
        <th class="configHeader" colspan = '2'>Test Configuration</th>
      </tr>
      <!-- <tr> -->
      <!--   <td class="attributeHeader" width = '30%'>Attribute</td> -->
      <!--   <td class="attributeHeader" width = '70%'>Value</td> -->
      <!-- </tr> -->
      
      <tr>
        <td>report file</td>
        <td><xsl:value-of select='fileName'/></td>
      </tr>
      <tr>
        <td>testIDEA version</td>
        <td><xsl:value-of select='testIDEAVersion'/></td>
      </tr>

      <tr>
        <td>winIDEA version</td>
        <td><xsl:value-of select='winIDEAVersion'/></td>
      </tr>

      <xsl:for-each select="testInfo/*">
        <tr>
          <xsl:choose>
              <xsl:when test='key = "testSpecificationFile"'>
                <td><xsl:value-of select='key'/></td>

                <td>
                  <a href="{value}"><xsl:value-of select='value'/></a>
                </td>
              </xsl:when>
              <xsl:otherwise>
                <td><xsl:value-of select='key'/></td>
                <td><xsl:value-of select='value'/></td>
              </xsl:otherwise>
          </xsl:choose>
        </tr>
      </xsl:for-each>
      
    </table>
</xsl:template>


<xsl:template match="reportDoc/main/reportStatistic">

    <table width = '100%'>
      <tr>
        <th class="statisticHeader" colspan='2'>Test Statistic</th>
      </tr>
      <!-- <tr> -->
      <!--   <td class="attributeHeader" width='30%'>Attribute</td> -->
      <!--   <td class="attributeHeader" width='70%'>Value</td> -->
      <!-- </tr> -->
      
      <tr>
        <td>Number of all tests</td>
        <td align = 'right'><xsl:value-of select='noOfTests'/></td>
      </tr>
      <tr>
          <td>Number of not passed tests</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="allErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td class="attributeHeader">Failure/Error type</td>
        <td class="attributeHeader">No. of failures/errors</td>
      </tr>
      <tr>
        <td>Errors (test execution exceptions)</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="exceptionErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Expression failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="expressionErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Coverage failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="coverageErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Code profiler failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="codeProfilerErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Data profiler failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="dataProfilerErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Script failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="scriptErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Stub failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="stubErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Test point failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="testPointErrors"/>
          </xsl:call-template>
      </tr>
      <tr>
        <td>Stack usage failures</td>
          <xsl:call-template name="showErrorCount">
              <xsl:with-param name="value" select="stackUsageErrors"/>
          </xsl:call-template>
      </tr>
    </table>
</xsl:template>


<xsl:template name="showErrorCount">
    <xsl:param name="value"/>

    <xsl:choose>
        <xsl:when test="$value = 0">
            <td align = 'right'><xsl:value-of select="$value"/></td>
        </xsl:when>
        <xsl:otherwise>
            <td align = 'right' class='failBkgColor'><xsl:value-of select="$value"/></td>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template name="testCasesWithFailuresAndErrors">
    <!-- Create a table with links to test cases with errors. -->
    <p class = 'linksToErrorsStyle'>  <!-- new class is required for link styles -->
        <table width = '100%'>
            <th class="linksToErrorsHeader" colspan="3">Test Cases With Failures and Errors</th>
            <tr class = "headerRow">
                <th class="headerCell" width="30%">Test ID</th>
                <th class="headerCell" width="30%">Function</th>
                <th class="headerCell" width="40%">Failure/Error</th>
            </tr>

            <xsl:for-each select="reportDoc/main/testResult">

                <xsl:if test="isError = 1">
                    <tr>
                        <xsl:choose>
                            <xsl:when test="isException = 1">
                                <td class="errorBkgColor"><a href="#_id_{position()}"><xsl:value-of select="testId"/></a></td>
                                <td class="functionNameError errorBkgColor"><a href="#_id_{position()}"><xsl:value-of select="function"/></a></td>
                            </xsl:when>
                            <xsl:otherwise>
                                <td class="failBkgColor"><a href="#_id_{position()}"><xsl:value-of select="testId"/></a></td>
                                <td class="functionNameFail failBkgColor"><a href="#_id_{position()}"><xsl:value-of select="function"/></a></td>
                            </xsl:otherwise>
                        </xsl:choose>

                        <xsl:choose>
                            <xsl:when test="isException = 1">
                                <td class="errorBkgColor">
                                    Error - test did not execute!&#160;
                                </td>
                            </xsl:when>
                            <xsl:otherwise>
                                <td class="failBkgColor">
                                    <xsl:if test="isTargetExceptionError = 1">
                                        Target Exception,&#160;
                                    </xsl:if>
                                    <xsl:if test="isExprError = 1">
                                        Expression,&#160;
                                    </xsl:if>
                                    <xsl:if test="isCoverageError = 1">
                                        Coverage,&#160;
                                    </xsl:if>
                                    <xsl:if test="isProfilerCodeError = 1">
                                        Code Profiler,&#160;
                                    </xsl:if>
                                    <xsl:if test="isProfilerDataError = 1">
                                        Data Profiler,&#160;
                                    </xsl:if>
                                    <xsl:if test="isScriptError = 1">
                                        Script,&#160;
                                    </xsl:if>
                                    <xsl:if test="isStubError = 1">
                                        Stub,&#160;
                                    </xsl:if>
                                    <xsl:if test="isTestPointError = 1">
                                        Test point,&#160;
                                    </xsl:if>
                                    <xsl:if test="isStackUsageError = 1">
                                        Stack usage&#160;
                                    </xsl:if>
                                </td>
                            </xsl:otherwise>
                        </xsl:choose>
                    </tr>
                </xsl:if>
            </xsl:for-each>

        </table>
    </p>  <!-- end of error link style -->
</xsl:template>


<xsl:template name="groupResultsTables">
    <!-- Create tables with group results. -->
    <xsl:for-each select="reportDoc/main/groupResult">
        <table width = '100%'>
            <tr class = "headerRow">
                <th class="groupHeader" style="width: 300px">Group ID</th>
                <th class="groupHeader"></th>
                <th class="groupHeader" style="width: 200px;">Result</th>
            </tr>
            <tr>
                <td class="testId"><xsl:value-of select="id"/></td>
                <td></td>

                <xsl:choose>
                    <xsl:when test="isGroupError = 0">
                        <td class="okStyle">Pass</td>
                    </xsl:when>
                    
                    <xsl:otherwise>
                        
                        <xsl:choose>

                            <xsl:when test="isException = 1">
                                <td class="exceptionStyle">Error</td>
                            </xsl:when>
                            <xsl:otherwise>
                                <td class="errorStyle">Fail</td>
                            </xsl:otherwise>
                            
                        </xsl:choose>
                        
                    </xsl:otherwise>
                </xsl:choose>
            </tr>

            <xsl:if test='desc != ""'>
                <tr>
                    <td class="attributeHeader" colspan = '3'>Description</td>
                </tr>
                <tr>
                    <td colspan="3"><pre><xsl:value-of select="desc"/></pre></td>
                </tr>
            </xsl:if>
            
            <xsl:if test='resultComment != ""'>
                <tr>
                    <td class="attributeHeader" colspan = '3'>Result comment - specific to this test run</td>
                </tr>
                <tr>
                    <td colspan="3"><pre><xsl:value-of select="resultComment"/></pre></td>
                </tr>
            </xsl:if>

            <xsl:if test='failedSections != ""'>
                <tr>
                    <td class="attributeHeader">Failed test sections:</td>
                    <td class='errorBkg' colspan="2"><xsl:value-of select="failedSections"/></td>
                </tr>
            </xsl:if>

            <xsl:apply-templates select="filter"/>
            <xsl:apply-templates select="resultData"/>
            
        </table>
        <p/>&#160;
        <p/>&#160;
    </xsl:for-each>
</xsl:template>


<xsl:template name="testCaseResultsTables">
    <!-- Create tables with test case results. -->
    <xsl:for-each select="reportDoc/main/testResult">

        <!-- if htmlViewMode is not specified, default is show all test cases. -->
        <xsl:if test='not(/reportDoc/main/reportConfig/htmlViewMode = "errorsOnly")  or  isError = 1'>
            <!-- put the id in front of each table, so that it is available for link ids -->
            <xsl:if test="isError = 1">
                <a id="_id_{position()}"/>
            </xsl:if>


            <table width = '100%'>
                <tr class = "headerRow">
                    <th class="headerCell" width="30%">Test ID</th>
                    <th class="headerCell" width="50%">Function</th>
                    <th class="headerCell" width="20%">Result</th>
                </tr>
                <tr>
                    <td class="testId"><xsl:value-of select="testId"/></td>
                    <td class="functionName"><xsl:value-of select="function"/></td>

                    <xsl:choose>
                        <xsl:when test="isError = 0">
                            <td class="okStyle">Pass</td>
                        </xsl:when>

                        <xsl:otherwise>

                            <xsl:choose>

                                <xsl:when test="isException = 1">
                                    <td class="exceptionStyle">Error</td>
                                </xsl:when>
                                <xsl:otherwise>
                                    <td class="errorStyle">Fail</td>
                                </xsl:otherwise>

                            </xsl:choose>

                        </xsl:otherwise>
                    </xsl:choose>
                </tr>

                <xsl:if test = 'tags != "" or baseTests != ""'>
                    <tr>
                        <td class="attributeHeader">Tags</td>
                        <td class="attributeHeader" colspan = '2'>Base tests</td>
                    </tr>
                    <tr>
                        <td><xsl:value-of select="tags"/></td>
                        <td colspan = '2'><xsl:value-of select="baseTests"/></td>
                    </tr>
                </xsl:if>

                <xsl:choose>
                    <xsl:when test='description != ""'>
                        <tr>
                            <td class="attributeHeader" colspan = '3'>Description</td>
                        </tr>
                        <tr>
                            <td colspan="3"><pre><xsl:value-of select="description"/></pre></td>
                        </tr>
                    </xsl:when>
                </xsl:choose>

                <xsl:choose>
                    <xsl:when test='resultComment != ""'>
                        <tr>
                            <td class="attributeHeader" colspan = '3'>Result comment - specific to this test run</td>
                        </tr>
                        <tr>
                            <td colspan="3"><pre><xsl:value-of select="resultComment"/></pre></td>
                        </tr>
                    </xsl:when>
                </xsl:choose>


                <xsl:apply-templates select="tests"/>
                <xsl:apply-templates select="log"/>
                <xsl:apply-templates select="preConditionResults">
                    <xsl:with-param name="title" select="'Pre-Condition expressions'"/>
                </xsl:apply-templates>
                <xsl:apply-templates select="stubResults"/>
                <xsl:apply-templates select="testPoints"/>
                <xsl:apply-templates select="assertResults">
                    <xsl:with-param name="title" select="'Assert expressions'"/>
                </xsl:apply-templates>
                <xsl:apply-templates select="trace"/>
                <xsl:apply-templates select="coverage"/>
                <xsl:apply-templates select="profiler"/>
                <xsl:apply-templates select="scriptOutput"/>
                <xsl:apply-templates select="scriptErrors"/>
                <xsl:apply-templates select="stackUsage"/>
                <xsl:apply-templates select="diagrams"/>

                <!-- exceptions -->
                <xsl:choose>
                    <xsl:when test="isException = 1">
                        <xsl:apply-templates select="exceptionStr"/>
                    </xsl:when>
                </xsl:choose>

                <xsl:if test="isTargetExceptionError = 1">
                    <tr><td colspan="3" class="exceptionError"><b>Target Exception</b></td></tr>
                    <tr><td colspan="3" class="exceptionDesc"><pre><xsl:value-of select="targetExceptionStr"/></pre></td></tr>
                </xsl:if>

            </table>
            <p/>&#160;

            <p/>
        </xsl:if>

    </xsl:for-each>
</xsl:template>

  
<xsl:template match="testResult/environment">
      <tr>
        <td class="envHeader" colspan="18">Test Environment</td>
      </tr>
      <tr>
        <td class="attributeHeader" colspan="3">Attribute</td>
        <td class="attributeHeader" colspan="15">Value</td>
      </tr>

      <xsl:for-each select="*">
        <tr>
            <td colspan="3"><xsl:value-of select='name()'/></td>
            <td colspan="15"><xsl:value-of select='.'/></td>
        </tr>
      </xsl:for-each>
      
</xsl:template>


<xsl:template match="log">
    <tr><td colspan="3" class="expressionsTitle"><b>Log <i>before</i> test</b></td></tr>
    
    <!-- Header is somewhat redundant as it is clear without it what is
      variable name or expression and what is value.
    
      tr class="expressionsHeader">
        <td>Expression</td>
        <td colspan="2">Value</td>
    </tr -->

    <xsl:for-each select="before/pair">
      <tr>
        <td class='expression'><xsl:value-of select='key'/></td>
        <td colspan="2"><xsl:value-of select='value'/></td>
      </tr>
    </xsl:for-each>
   
    <tr><td colspan="3" class="expressionsTitle"><b>Log <i>after</i> test</b></td></tr>

    <xsl:for-each select="after/pair">
      <tr>
        <td class='expression'><xsl:value-of select='key'/></td>
        <td colspan="2"><xsl:value-of select='value'/></td>
      </tr>
    </xsl:for-each>

</xsl:template>


<xsl:template match="testResult/assertResults|testResult/preConditionResults">
    <xsl:param name="title"/>

    <tr><td colspan="3" class="expressionsTitle"><b><xsl:value-of select="$title"/></b></td></tr>
    
    <tr class="expressionsHeader">
        <td>Expression</td>
        <td colspan="2">Sub-expressions</td>
    </tr>

    <xsl:for-each select="item">

      <tr>
        <xsl:choose>
          <xsl:when test='isError = "false"'>
            <td><xsl:value-of select="expr"/></td>
          </xsl:when>
          <xsl:otherwise>
            <td class="expressionError"><xsl:value-of select="expr"/></td>
          </xsl:otherwise>
        </xsl:choose>

        <td colspan="2" class="expression">
          <xsl:for-each select="subExpr/pair">
             <xsl:value-of select='key'/> = <xsl:value-of select='value'/><br/>
          </xsl:for-each>
        </td>
      </tr>
      
    </xsl:for-each>
</xsl:template>



<xsl:template match="testResult/trace">

    <tr><td colspan="3" class="coverageTitle"><b>Trace</b></td></tr>

    <xsl:for-each select="files/document">
        <tr>
            <td colspan="1">Document</td>
            <td colspan="2"><xsl:value-of select='.'/></td>
        </tr>
    </xsl:for-each>
    <xsl:for-each select="files/exportFile">
        <tr>
            <td colspan="1">Export file</td>
            <td colspan="2">
                <a href="{.}"><xsl:value-of select='.'/></a></td>
        </tr>
    </xsl:for-each>
</xsl:template>


<xsl:template name="groupCoverage">
    <!-- creates table in table to avoid problems of aligning lines with different numbers of columns -->
    <tr><td colspan="3">
    <table width = '100%'>

        <xsl:call-template name="coverageTableHeaderAndFiles">
            <xsl:with-param name="trdFile" select = "analyzerFile"/>
            <xsl:with-param name="exportFile" select = "cvrgExportFile"/>
            <xsl:with-param name="firstColHeader" select = "''"/>
        </xsl:call-template>

        <xsl:for-each select="coverageAll">
            <xsl:call-template name="coverageStatistics"/>
        </xsl:for-each>

        <xsl:for-each select="coverageTestedOnly">
            <xsl:call-template name="coverageStatistics"/>
        </xsl:for-each>

    </table>  <!-- end of table in table -->
    </td></tr>
</xsl:template>


<xsl:template match="testResult/coverage">
    <!-- creates table in table to avoid problems of aligning lines with different numbers of columns -->
    <tr><td colspan="3">
    <table width = '100%'>

        <xsl:call-template name="coverageTableHeaderAndFiles">
            <xsl:with-param name="trdFile" select = "files/document"/>
            <xsl:with-param name="exportFile" select = "files/exportFile"/>
            <xsl:with-param name="firstColHeader" select = "'Function'"/>
        </xsl:call-template>


        <xsl:for-each select="results/item">
            <xsl:call-template name="coverageStatistics"/>
        </xsl:for-each>
        
    </table>  <!-- end of table in table -->
    </td></tr>
    
</xsl:template>


<xsl:template name="coverageTableHeaderAndFiles">
    <xsl:param name="trdFile"/>
    <xsl:param name="exportFile"/>
    <xsl:param name="firstColHeader"/>
    
    <tr><td colspan="12" class="coverageTitle"><b>Coverage</b></td></tr>

    <tr>
        <td colspan="1" class="coverageTitle">Document</td>
        <td colspan="11" class="coverageTitle"><xsl:value-of select='$trdFile'/></td>
    </tr>
    <tr>
        <td colspan="1" class="coverageTitle">Export file</td>
        <td colspan="11" class="coverageTitle">
        <a href="{$exportFile}"><xsl:value-of select='$exportFile'/></a></td>
    </tr>

        <tr class="coverageHeader">
            <td rowspan="2"><xsl:value-of select="$firstColHeader"/></td>
            <td class="groupBorder" rowspan="2">Obj. code all</td>
            <td class="groupBorder" rowspan="2">Src. lines all</td>
            <td class="groupBorder" rowspan="2">Cond. all</td>
            <td class="groupBorder" rowspan="2">CC (Outcomes)</td>
            <td class="groupBorder" colspan="1">Obj. code executed</td>
            <td class="groupBorder" colspan="1">Src. lines executed</td>
            <td class="groupBorder" colspan="1">Conditions any</td>
            <td class="groupBorder" colspan="1">Cond. true only</td>
            <td class="groupBorder" colspan="1">Cond. false only</td>
            <td class="groupBorder" colspan="1">Conditions both</td>
        </tr>

        <tr class="coverageHeader">
            <td class="groupBorder">measured (exp., abs.)</td>
            <td class="groupBorder">measured (exp., abs.)</td>
            <td class="groupBorder">measured (exp., abs.)</td>
            <td class="groupBorder">measured (exp., abs.)</td>
            <td class="groupBorder">measured (exp., abs.)</td>
            <td class="groupBorder">measured (exp., abs.)</td>
        </tr>
    
</xsl:template>


<xsl:template name="coverageStatistics">

    <tr class="cvrgValues">
        <xsl:choose>
            <xsl:when test='isError = "0"'>
                <td class="analyzedFunctionName"><xsl:value-of select="funcName"/></td>
            </xsl:when>
            <xsl:otherwise>
                <td class="errFunctionName"><xsl:value-of select="funcName"/></td>
            </xsl:otherwise>
        </xsl:choose>


        <td class="leftThickBorder"><xsl:value-of select='bytesAll'/></td>
        <td><xsl:value-of select='sourceLinesAll'/></td>
        <td><xsl:value-of select='branchesAll'/></td>

        <xsl:variable name="conditionsAll" select='branchesAll'/>
        <xsl:variable name="condTrueOnly" select='branchesTaken/measuredAbs'/>
        <xsl:variable name="condFalseOnly" select='branchesNotTaken/measuredAbs'/>
        <xsl:variable name="condBoth" select='branchesBoth/measuredAbs'/>
        <xsl:call-template name="singleColorBarGraph">
            <xsl:with-param name="nominator" select="$condTrueOnly + $condFalseOnly + $condBoth * 2"/>
            <xsl:with-param name="denominator" select="$conditionsAll * 2"/>
            <xsl:with-param name="barGraphWidth" select="$_cvrgBarGraphW"/>
        </xsl:call-template>

        

        <xsl:apply-templates select='bytesExecuted'>
            <xsl:with-param name="isError" select="isBytesExecutedError"/>
        </xsl:apply-templates>

        <xsl:apply-templates select='sourceLinesExecuted'>
            <xsl:with-param name="isError" select="isSourceLinesExecutedError"/>
        </xsl:apply-templates>

        <xsl:apply-templates select='branchesExecuted'>
            <xsl:with-param name="isError" select="isBranchesExecutedError"/>
        </xsl:apply-templates>

        <xsl:apply-templates select='branchesTaken'>
            <xsl:with-param name="isError" select="isBranchesTakenError"/>
        </xsl:apply-templates>

        <xsl:apply-templates select='branchesNotTaken'>
            <xsl:with-param name="isError" select="isBranchesNotTakenError"/>
        </xsl:apply-templates>

        <xsl:apply-templates select='branchesBoth'>
            <xsl:with-param name="isError" select="isBranchesBothError"/>
        </xsl:apply-templates>

    </tr>
</xsl:template>


<xsl:template match="bytesExecuted|sourceLinesExecuted|branchesExecuted|branchesTaken|branchesNotTaken|branchesBoth">
    <xsl:param name="isError"/>
        
    <xsl:choose>
        <xsl:when test='$isError = "0"'>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="nominator" select="measuredRel"/>
                <xsl:with-param name="denominator" select="1"/>
                <xsl:with-param name="boldPrefixText">
                    <xsl:apply-templates  select="measuredRel"/>
                </xsl:with-param>
                <xsl:with-param name="text">
                    (<xsl:apply-templates select='expected'/>,
                    <xsl:value-of  select='measuredAbs'/>)
                </xsl:with-param>
                <xsl:with-param name="barGraphWidth" select="$_cvrgBarGraphW"/>
            </xsl:call-template>
            
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="nominator" select="measuredRel"/>
                <xsl:with-param name="denominator" select="1"/>
                <xsl:with-param name="rightColor" select="$_errorBkgColor"/>
                <xsl:with-param name="boldPrefixText">
                    <xsl:apply-templates  select="measuredRel"/>
                </xsl:with-param>
                <xsl:with-param name="text">
                    (<xsl:apply-templates select='expected'/>,
                    <xsl:value-of  select='measuredAbs'/>)
                </xsl:with-param>
                <xsl:with-param name="barGraphWidth" select="$_cvrgBarGraphW"/>
            </xsl:call-template>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template match="testResult/profiler">
    <!-- creates table in table to avoid problems of aligning lines with different numbers of columns -->
    <tr><td colspan="3">
    <table width = '100%'>
        
        <tr><td colspan="16" class="codeProfilerTitle"><b>Profiler</b></td></tr>

        <xsl:for-each select="files/document">
            <tr>
                <td colspan="1" class="coverageTitle">Document</td>
                <td colspan="14" class="coverageTitle"><xsl:value-of select='.'/></td>
            </tr>
        </xsl:for-each>
        <xsl:for-each select="files/exportFile">
            <tr>
                <td colspan="1" class="coverageTitle">Export file</td>
                <td colspan="14" class="coverageTitle">
                    <a href="{.}"><xsl:value-of select='.'/></a></td>
            </tr>
        </xsl:for-each>
        
        <xsl:apply-templates select="codeProfiler"/>
        <xsl:apply-templates select="dataProfiler"/>
    
    </table>  <!-- end of table in table -->
    </td></tr>
</xsl:template>


<xsl:template match="codeProfiler">

    <!-- creates table in table to avoid problems of aligning lines with different numbers of columns -->
    <tr><td colspan="3">
    <table width = '100%'>
        
        <tr><td colspan="11" class="codeProfilerTitle"><b>Code Profiler</b></td></tr>

        
        <tr class="codeProfilerHeader">
            <td>Function</td>
            <td></td>
            <td></td>
            <td class="groupBorder">Min</td>
            <td class="groupBorder">Max</td>
            <td class="groupBorder">Average</td>
            <td class="groupBorder">Total</td>
            <td class="groupBorder">Min Start</td>
            <td class="groupBorder">Min End</td>
            <td class="groupBorder">Max Start</td>
            <td class="groupBorder">Max End</td>
        </tr>

        <xsl:for-each select="item">

            <!-- tr class="numberRow">
                <xsl:choose>
                    <xsl:when test='isError = "0"'>
                        <td class="analyzedFunctionName" rowspan='16'><xsl:value-of select="funcName"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td class="errFunctionName" rowspan='16'><xsl:value-of select="funcName"/></td>
                    </xsl:otherwise>
                </xsl:choose -->

                <xsl:apply-templates select="measuredProfilerResults/item/netTimeStatus">
                    <xsl:with-param name="title" select="'Net'"></xsl:with-param>
                    <xsl:with-param name="funcVarName" select="funcName"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/grossTimeStatus">
                    <xsl:with-param name="title" select="'Gross'"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/callTimeStatus">
                    <xsl:with-param name="title" select="'Call'"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/periodTimeStatus">
                    <xsl:with-param name="title" select="'Period'"></xsl:with-param>
                </xsl:apply-templates>

                <xsl:apply-templates select="measuredProfilerResults/item/hits">
                    <xsl:with-param name="title" select="'Hits'"></xsl:with-param>
                </xsl:apply-templates>
            <!-- /tr -->
        </xsl:for-each>
        
    </table>  <!-- end of table in table -->
    </td></tr>
    
</xsl:template>


<xsl:template match="dataProfiler">

    <!-- creates table in table to avoid problems of aligning lines with different numbers of columns -->
    <tr><td colspan="3">
    <table width = '100%'>
        
        <tr><td colspan="11" class="dataProfilerTitle"><b>Data Profiler</b></td></tr>

        
        <tr class="dataProfilerHeader">
            <td>Variable</td>
            <td></td>
            <td></td>
            <td class="groupBorder">Min</td>
            <td class="groupBorder">Max</td>
            <td class="groupBorder">Average</td>
            <td class="groupBorder">Total</td>
            <td class="groupBorder">Min Start</td>
            <td class="groupBorder">Min End</td>
            <td class="groupBorder">Max Start</td>
            <td class="groupBorder">Max End</td>
        </tr>

        <xsl:for-each select="item">

            <!-- tr class="numberRow" -->
                <!-- xsl:choose>
                    <xsl:when test='isError = "0"'>
                        <td class="analyzedFunctionName" rowspan='16'><xsl:value-of select="varName"/>@</td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td class="errFunctionName" rowspan='16'><xsl:value-of select="varName"/></td>
                    </xsl:otherwise>
                </xsl:choose -->
<!-- select="measuredProfilerResults/item/netTimeStatus" -->
                <xsl:apply-templates select="measuredProfilerResults/item/netTimeStatus">
                    <xsl:with-param name="title" select="'Net'"></xsl:with-param>
                    <xsl:with-param name="funcVarName" select="varName"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/grossTimeStatus">
                    <xsl:with-param name="title" select="'Gross'"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/outsideTimeStatus">
                    <xsl:with-param name="title" select="'Outside'"></xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="measuredProfilerResults/item/periodTimeStatus">
                    <xsl:with-param name="title" select="'Period'"></xsl:with-param>
                </xsl:apply-templates>

                <xsl:apply-templates select="measuredProfilerResults/item/hits">
                    <xsl:with-param name="title" select="'Hits'"></xsl:with-param>
                </xsl:apply-templates>
            <!-- /tr -->
        </xsl:for-each>
        
    </table>  <!-- end of table in table -->
    </td></tr>
    
</xsl:template>


<xsl:template match="netTimeStatus|grossTimeStatus|callTimeStatus|periodTimeStatus|outsideTimeStatus">
  <xsl:param name="title"/>
  <xsl:param name="funcVarName"/>
  
  <tr>
    <xsl:choose>
      <xsl:when test='$funcVarName != ""'>
        <td class="analyzedFunctionName" rowspan='15'><xsl:value-of select="$funcVarName"/></td>
      </xsl:when>
    </xsl:choose>

    <td rowspan='3'><xsl:value-of select="$title"/></td><td>Low</td>
    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="minTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="maxTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="averageTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="averageTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="totalTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="totalTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minStartTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="minStartTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minEndTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="minEndTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxStartTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="maxStartTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxEndTime/expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="maxEndTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>
  </tr>
  <tr><td>Result</td>
    <td><xsl:value-of select="minTime/measuredTime"/></td>
    <td><xsl:value-of select="maxTime/measuredTime"/></td>
    <td><xsl:value-of select="averageTime/measuredTime"/></td>
    <td><xsl:value-of select="totalTime/measuredTime"/></td>
    <td><xsl:value-of select="minStartTime/measuredTime"/></td>
    <td><xsl:value-of select="minEndTime/measuredTime"/></td>
    <td><xsl:value-of select="maxStartTime/measuredTime"/></td>
    <td><xsl:value-of select="maxEndTime/measuredTime"/></td>
  </tr>
  <tr><td>High</td>
    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="minTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="maxTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="averageTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="averageTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>
    
    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="totalTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="totalTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minStartTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="minStartTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="minEndTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="minEndTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxStartTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="maxStartTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>

    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="maxEndTime/expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="maxEndTime/result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>
  </tr>

</xsl:template>
  

<xsl:template match="hits">
  <xsl:param name="title"/>
  <tr><td rowspan='3'><xsl:value-of select="$title"/></td><td>Low</td>
    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="expectedLowerBound"/>
      <xsl:with-param name="resultStatus" select="result"/>
      <xsl:with-param name="errorCode" select="'ERR_MIN'"/>
    </xsl:call-template>
  </tr>
  <tr><td>Result</td>
    <td><xsl:value-of select="measuredTime"/></td>
  </tr>
  <tr><td>High</td>
    <xsl:call-template name="profilerValue">
      <xsl:with-param name="value" select="expectedUpperBound"/>
      <xsl:with-param name="resultStatus" select="result"/>
      <xsl:with-param name="errorCode" select="'ERR_MAX'"/>
    </xsl:call-template>
  </tr>
</xsl:template>


<xsl:template name="profilerValue">
    <xsl:param name="value"/>
    <xsl:param name="resultStatus"/>
    <xsl:param name="errorCode"/>

    <xsl:choose>
      <xsl:when test="$resultStatus = $errorCode  or  $resultStatus = 'ERR_BOTH'">
        <td class="profilerError"><xsl:value-of select='$value'/></td>
      </xsl:when>
      <xsl:otherwise>
        <td class="profilerValue"><xsl:value-of select='$value'/></td>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template match="testResult/scriptOutput">
    <tr><td colspan="3" class="scriptOutput"><b>Information reported by script functions</b></td></tr>

    <xsl:for-each select="pair">
      <tr>
        <td class='scriptErrorDesc'><xsl:value-of select='key'/></td>
        <td colspan="2"><xsl:value-of select='value'/></td>
      </tr>
    </xsl:for-each>
</xsl:template>


<xsl:template match="testResult/scriptErrors">
    <tr><td colspan="3" class="scriptError"><b>Failures reported by script functions</b></td></tr>
    <xsl:for-each select="*">
        <tr>
            <td class="scriptErrorDesc"><i><xsl:value-of select='name()'/></i></td>
            <td colspan="2"><pre><xsl:value-of select='.'/></pre></td>
        </tr>
    </xsl:for-each>
</xsl:template>


<xsl:template match="testResult/exceptionStr">
    <tr><td colspan="3" class="exceptionError"><b>Exception</b></td></tr>
    <tr><td colspan="3" class="exceptionDesc"><pre><xsl:value-of select="."/></pre></td></tr>
</xsl:template>


<xsl:template match="testResult/stubResults">

    <xsl:call-template name="tpAndStubResults">
      <xsl:with-param name="resultName" select="'Stubs'"/>
      <xsl:with-param name="tpIdOrStubbedFunc" select="'Stubbed func.'"/>
    </xsl:call-template>
</xsl:template>

    
<xsl:template match="testResult/testPoints">
    <xsl:call-template name="tpAndStubResults">
      <xsl:with-param name="resultName" select="'Test Points'"/>
      <xsl:with-param name="tpIdOrStubbedFunc" select="'Test p. ID'"/>
    </xsl:call-template>
</xsl:template>

    
<xsl:template name="tpAndStubResults">
    <xsl:param name="resultName" />
    <xsl:param name="tpIdOrStubbedFunc" />
    
    <!-- creates table in table to avoid problems of aligning lines
         with different numbers of columns -->
         
    <tr><td colspan="3">
      <table width = '100%'>

        <tr><td colspan="24" class="testPointTitle"><b><xsl:value-of select="$resultName" /></b></td></tr>

        <tr class='testPointHeader'>
          <td><xsl:value-of select="$tpIdOrStubbedFunc" /></td>
          <td>Status</td>
          <td>Hit No</td>
          <td>Step</td>
          <td>Before</td>
          <td>After</td>
          <td>Script out</td>
          <td>Script fail.</td>
          <td>Failures</td>
        </tr>
        <xsl:for-each select="item">
            <tr>
                <td><xsl:value-of select="tpIdOrStubbedFunc"/><br/>
                <xsl:value-of select="location"/>
                </td>
                <td><xsl:value-of select="execStatus"/></td>
                <td><xsl:value-of select="hitNo"/></td>
                <td><xsl:value-of select="stepIdx"/></td>
                <td class='expression'>
                  <xsl:for-each select="log/before/*">
                    <xsl:value-of select='key'/> = <xsl:value-of select='value'/><br/>
                  </xsl:for-each>
                </td>
                <td class='expression'>
                  <xsl:for-each select="log/after/*">
                    <xsl:value-of select='key'/> = <xsl:value-of select='value'/><br/>
                  </xsl:for-each>
                </td>

                <td><xsl:value-of select="scriptOut"/></td>
                <xsl:choose>
                  <xsl:when test = 'exprErrors'>
                    <td class='expressionError'><xsl:value-of select="scriptErr"/></td>
                  </xsl:when>
                  <xsl:otherwise>
                    <td/>
                  </xsl:otherwise>
                </xsl:choose>

                <xsl:if test = 'exprErrors'>
                  <td class='expressionError'>
                    <xsl:for-each select="exprErrors/*">
                      <b>
                        <xsl:value-of select='key'/>
                      </b><p/>
                      <pre class='testPointSubExpr'>
                        <xsl:value-of select='value'/>
                      </pre>
                    </xsl:for-each>
                  </td>
                </xsl:if>
            </tr>
        </xsl:for-each>
      </table>
    </td>
    </tr>
</xsl:template>


<xsl:template match="testResult/stackUsage">
    <tr><td colspan="3">
    <table width = '100%'>
    <tr><td colspan="4" class="stackUsage"><b>Stack usage</b></td></tr>
        <tr>
            <td class="stackUsage">Used before test</td>
            <td class="stackUsage">Used for test vars and call frame</td>
            <td class="stackUsage">Used by tested function</td>
            <td class="stackUsage">Stack usage limit (for tested f. only)</td>
        </tr>
        <tr>
            <td><xsl:value-of select='usageBeforeTest'/></td>
            <td><xsl:value-of select='testIDEAUsage'/></td>

            <xsl:choose>
                <xsl:when test="applicationUsage &gt; maxSize">
                    <td class="stackUsageError"><xsl:value-of select='applicationUsage'/></td>
                </xsl:when>
                <xsl:otherwise>
                    <td><xsl:value-of select='applicationUsage'/></td>
                </xsl:otherwise>
            </xsl:choose>

            <td><xsl:value-of select='maxLimit'/></td>
        </tr>
    </table>
    </td>
    </tr>
</xsl:template>


<xsl:template match="testResult/diagrams">
    <xsl:for-each select="item">
        <tr><td colspan="3">
            <br/>
            <xsl:value-of select='.'/>
        </td></tr>
        <tr><td colspan="3" align='center'>
            <img src="{.}"/>
        </td></tr>
    </xsl:for-each>
</xsl:template>


<xsl:template match="minTime|maxTime|averageTime|totalTime|minStartTime|minEndTime|maxStartTime|maxEndTime">

  <xsl:choose>
    <xsl:when test="result = 'ERR_MIN'  or  result = 'ERR_BOTH'">
      <td class="profilerError" style="border-left-width: 3px;"><xsl:apply-templates select="expectedLowerBound"/></td>
    </xsl:when>
    <xsl:otherwise>
      <td class="profilerValue" style="border-left-width: 3px;"><xsl:apply-templates select="expectedLowerBound"/></td>
    </xsl:otherwise>
  </xsl:choose>

  <td class="profilerMeasuredVal">
      <xsl:apply-templates select="measuredTime"/>
  </td>

  <xsl:choose>
    <xsl:when test="result = 'ERR_MIN'  or  result = 'ERR_BOTH'">
      <td class="profilerError"><xsl:apply-templates select="expectedUpperBound"/></td>
    </xsl:when>
    <xsl:otherwise>
      <td class="profilerValue"><xsl:apply-templates select="expectedUpperBound"/></td>
    </xsl:otherwise>
  </xsl:choose>
  
</xsl:template>


<!-- Template for formatting profiler times given in nanoseconds.
     Tests for existence of number to avoid Nan output.
-->
<xsl:template match="measuredTime|expectedLowerBound|expectedUpperBound">
  <xsl:if test = '. != ""'>
    <xsl:value-of select='format-number(., "###,##0")'/>
  </xsl:if>
</xsl:template>


<!-- Template for formatting coverage relative numbers given in range [0..100]
     Tests for existence of number to avoid Nan output.
-->
<xsl:template match="expected | measuredRel">
	<xsl:if test='. != ""'>
		<!-- show '/' for values -0.01, because they indicate undefined value - 
			it happens when num. of bytes or branches is 0, so relative number is undefined -->
		<xsl:choose>
			<xsl:when test='. != "-0.01"'>
				<xsl:value-of select='format-number(number(.), "0.0%")' />
			</xsl:when>
			<xsl:otherwise>
				<b> / </b>
			</xsl:otherwise>
		</xsl:choose>
    </xsl:if>
</xsl:template>


<xsl:template match="filter">
    <tr>
        <td class="attributeHeader" colspan = '3'>Filter</td>
    </tr>
    
    <xsl:apply-templates select='coreId'/>        
        
    <xsl:apply-templates select="partitions">
      <xsl:with-param name="criteriaName" select="'Partitions'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='modules'>
      <xsl:with-param name="criteriaName" select="'Modules'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='includedFunctions'>
      <xsl:with-param name="criteriaName" select="'Included functions'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='excludedFunctions'>
      <xsl:with-param name="criteriaName" select="'Excluded functions'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='includedIds'>
      <xsl:with-param name="criteriaName" select="'Included test IDs'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='excludedIds'>
      <xsl:with-param name="criteriaName" select="'Excluded test IDs'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='mustHaveAllTags'>
      <xsl:with-param name="criteriaName" select="'Must have all tags'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='mustHaveOneOfTags'>
      <xsl:with-param name="criteriaName" select="'Must have at least one of tags'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='mustNotHaveAllTags'>
      <xsl:with-param name="criteriaName" select="'Must NOT have any of tags'"/>
    </xsl:apply-templates>

    <xsl:apply-templates select='mustNotHaveOneOfTags'>
      <xsl:with-param name="criteriaName" select="'Must NOT have at least one of tags'"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="coreId">
    <tr>
        <td>Core ID</td>
        <td colspan = '2' style="font-family: monospace">xsl:value-of select="."/></td>
    </tr>
</xsl:template>


<xsl:template match="partitions|modules|includedFunctions|excludedFunctions|includedIds|excludedIds|mustHaveAllTags|mustHaveOneOfTags|mustNotHaveAllTags|mustNotHaveOneOfTags">
    <xsl:param name="criteriaName"/>
    <xsl:param name="criteriaPath"/>

    <tr>
        <td><xsl:value-of select='$criteriaName'/></td>
        <td colspan = '2' style="font-family: monospace">
            <xsl:for-each select="item">
                <xsl:value-of select='.'/><br/>
            </xsl:for-each>
        </td>
    </tr>
</xsl:template>


<xsl:template match="resultData">

    <xsl:if test='exception'>
        <tr><td class = 'errorBkg'>Exception</td>
            <td class = 'errorBkg' colspan="2"><xsl:value-of select='exception'/></td></tr>
    </xsl:if>

    <xsl:if test='analyzerFile'>
        <xsl:call-template name="groupCoverage"/>
    </xsl:if>
    
    <xsl:call-template name='groupTestCaseStatisticsAndResults'/>
    <!-- xsl:call-template name='groupTestResults'/ added as four graph column to the above table -->
    <xsl:apply-templates select="funcStats">
        <xsl:with-param name="maxTestCases" select="maxTestCasesForFunc"/>
    </xsl:apply-templates>
</xsl:template>


<xsl:template name="groupTestCaseStatisticsAndResults">
    <tr><td colspan="3">
    <table width = '100%' border='0'>

        <tr><td class="attributeHeader" colspan='6'><b>Group test case statistics and results</b></td></tr>
        <tr>
            <td width='210'></td>
            <td width='210' class='colHeaderBorder'>In group</td>
            <td width='210' class='colHeaderBorder'>With test cases</td>
            <td width='210' class='colHeaderBorder'>Without test cases</td>
            <td class='colHeaderBorder'>Tests per item</td>
            <td class='colHeaderBorder'>Pass / Fail / Error / Not executed</td>
        </tr>
        <xsl:variable name="allTests" select='noOfTestCasesInGroup'/>
        <tr>
            <td class='rowHeaderBorder'>Test cases</td>
            <td><xsl:value-of select='$allTests'/></td>
            <td>/</td>
            <td>/</td>
            <td>/</td>

            <xsl:call-template name="fourColorBarGraph">
                <xsl:with-param name="leftNum" select="passedTestCases"/>
                <xsl:with-param name="middleNum" select="failedTestCases"/>
                <xsl:with-param name="rightNum" select="errorTestCases"/>
                <xsl:with-param name="complete" select="noOfTestCasesInGroup"/>
            </xsl:call-template>
        </tr>
        <tr>
            <td class='rowHeaderBorder'>Functions</td>

            <xsl:variable name="fInGroup" select='noOfFunctionsInGroup'/>
            <xsl:variable name="fWithTests" select='funcsWTestCases'/>
            <xsl:variable name="percentage" select='format-number(number($fWithTests div $fInGroup * 100), "0")'/>
            
            <td><xsl:value-of select='$fInGroup'/></td>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_neutralBarBkgColor"/>
                <xsl:with-param name="nominator" select="$fWithTests"/>
                <xsl:with-param name="denominator" select="$fInGroup"/>
            </xsl:call-template>
            
            <td><xsl:value-of select='$fInGroup - $fWithTests'/></td>
            <td><xsl:value-of select='format-number($allTests div $fInGroup, "###0.#")'/></td>

            <xsl:call-template name="fourColorBarGraph">
                <xsl:with-param name="leftNum" select="passedFunctions"/>
                <xsl:with-param name="middleNum" select="failedFunctions"/>
                <xsl:with-param name="rightNum" select="errorFunctions"/>
                <xsl:with-param name="complete" select="noOfFunctionsInGroup"/>
            </xsl:call-template>
        </tr>
        <tr>
            <td class='rowHeaderBorder'>Modules</td>
            <xsl:variable name="mInGroup" select='noOfModulesInGroup'/>
            <xsl:variable name="mWithTests" select='modulesWTestCases'/>
            <td><xsl:value-of select='$mInGroup'/></td>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_neutralBarBkgColor"/>
                <xsl:with-param name="nominator" select="$mWithTests"/>
                <xsl:with-param name="denominator" select="$mInGroup"/>
            </xsl:call-template>

            <td><xsl:value-of select='$mInGroup - $mWithTests'/></td>
            <td><xsl:value-of select='format-number($allTests div $mInGroup, "###0.#")'/></td>

            <xsl:call-template name="fourColorBarGraph">
                <xsl:with-param name="leftNum" select="passedModules"/>
                <xsl:with-param name="middleNum" select="failedModules"/>
                <xsl:with-param name="rightNum" select="errorModules"/>
                <xsl:with-param name="complete" select="noOfModulesInGroup"/>
            </xsl:call-template>
        </tr>
        <tr>
            <td class='rowHeaderBorder'>Partitions</td>
            <xsl:variable name="pInGroup" select='noOfPartitionsInGroup'/>
            <xsl:variable name="pWithTests" select='partitionsWTestCases'/>
            <td><xsl:value-of select='$pInGroup'/></td>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_neutralBarBkgColor"/>
                <xsl:with-param name="nominator" select="$pWithTests"/>
                <xsl:with-param name="denominator" select="$pInGroup"/>
            </xsl:call-template>
            
            <!--td><xsl:value-of select='$pWithTests'/>&#160;(<xsl:value-of select='format-number(number($pWithTests div $pInGroup), "0.0 %")'/>)</td>
            <td></td-->
            <td><xsl:value-of select='$pInGroup - $pWithTests'/></td>
            <td><xsl:value-of select='format-number($allTests div $pInGroup, "###.#")'/></td>

            <xsl:call-template name="fourColorBarGraph">
                <xsl:with-param name="leftNum" select="passedPartitions"/>
                <xsl:with-param name="middleNum" select="failedPartitions"/>
                <xsl:with-param name="rightNum" select="errorPartitions"/>
                <xsl:with-param name="complete" select="noOfPartitionsInGroup"/>
            </xsl:call-template>
        </tr>
    </table>

    </td></tr>
    
</xsl:template>


<xsl:template name="groupTestResults">
    <tr><td colspan="3">
    <table width = '100%' border='0'>

        <tr><td class="attributeHeader" colspan='5'><b>Group test results</b></td></tr>
        <tr>
            <td width='210'></td>
            <td width='210' class='colHeaderBorder'>Passed</td>
            <td width='210' class='colHeaderBorder'>Failed</td>
            <td width='210' class='colHeaderBorder'>Error</td><td style='border: 0'/>
        </tr>
        <xsl:variable name="noOfTestCasesInGroup" select="noOfTestCasesInGroup"/>
        <xsl:variable name="noOfFunctionsInGroup" select="noOfFunctionsInGroup"/>
        <xsl:variable name="noOfModulesInGroup" select="noOfModulesInGroup"/>
        <xsl:variable name="noOfPartitionsInGroup" select="noOfPartitionsInGroup"/>
        <tr>
            <td class='rowHeaderBorder'>Test cases</td>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_okBkgColor"/>
                <xsl:with-param name="nominator" select="passedTestCases"/>
                <xsl:with-param name="denominator" select="$noOfTestCasesInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_failBkgColor"/>
                <xsl:with-param name="nominator" select="failedTestCases"/>
                <xsl:with-param name="denominator" select="$noOfTestCasesInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_errorBkgColor"/>
                <xsl:with-param name="nominator" select="errorTestCases"/>
                <xsl:with-param name="denominator" select="$noOfTestCasesInGroup"/>
            </xsl:call-template>
        </tr>

        <tr>
            <td class='rowHeaderBorder'>Functions</td>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_okBkgColor"/>
                <xsl:with-param name="nominator" select="passedFunctions"/>
                <xsl:with-param name="denominator" select="noOfFunctionsInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_failBkgColor"/>
                <xsl:with-param name="nominator" select="failedFunctions"/>
                <xsl:with-param name="denominator" select="noOfFunctionsInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_errorBkgColor"/>
                <xsl:with-param name="nominator" select="errorFunctions"/>
                <xsl:with-param name="denominator" select="noOfFunctionsInGroup"/>
            </xsl:call-template>
        </tr>

        <tr>
            <td class='rowHeaderBorder'>Modules</td>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_okBkgColor"/>
                <xsl:with-param name="nominator" select="passedModules"/>
                <xsl:with-param name="denominator" select="noOfModulesInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_failBkgColor"/>
                <xsl:with-param name="nominator" select="failedModules"/>
                <xsl:with-param name="denominator" select="noOfModulesInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_errorBkgColor"/>
                <xsl:with-param name="nominator" select="errorModules"/>
                <xsl:with-param name="denominator" select="noOfModulesInGroup"/>
            </xsl:call-template>
        </tr>

        <tr>
            <td class='rowHeaderBorder'>Partitions</td>
            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_okBkgColor"/>
                <xsl:with-param name="nominator" select="passedPartitions"/>
                <xsl:with-param name="denominator" select="noOfPartitionsInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_failBkgColor"/>
                <xsl:with-param name="nominator" select="failedPartitions"/>
                <xsl:with-param name="denominator" select="noOfPartitionsInGroup"/>
            </xsl:call-template>

            <xsl:call-template name="singleColorBarGraph">
                <xsl:with-param name="color" select="$_errorBkgColor"/>
                <xsl:with-param name="nominator" select="errorPartitions"/>
                <xsl:with-param name="denominator" select="noOfPartitionsInGroup"/>
            </xsl:call-template>
        </tr>
        
    </table>
        
    </td></tr>
        
</xsl:template>


<xsl:template match="funcStats">
    <xsl:param name="maxTestCases"/>
    
    <tr><td colspan="3">
    <table width = '100%' border='0'>

        <tr><td class="attributeHeader" colspan='10'><b>Group function statistics</b></td></tr>
        <tr>
            <td class='colHeaderBorder'>Partition</td>
            <td class='colHeaderBorder'>Module</td>
            <td class='colHeaderBorder'>Function</td>
            <td class='colHeaderBorder'># test cases</td>
            <td class='colHeaderBorder'>Pass / Fail / Error</td>
            <td class='colHeaderBorder'>Code cvrg.</td>
            <td class='colHeaderBorder'>Cond. cvrg.</td>
            <td class='colHeaderBorder'>Exec. count</td>
        </tr>

        <xsl:for-each select="item">
            <xsl:variable name="qFuncName" select='qualFuncName'/>
            <xsl:variable name="passed" select='passedTestCases'/>
            <xsl:variable name="failed" select='failedTestCases'/>
            <xsl:variable name="error" select='errorTestCases'/>

            <xsl:variable name="cvrgBytesAll" select='cvrgBytesAll'/>
            <xsl:variable name="cvrgBytesExecuted" select='cvrgBytesExecuted'/>
            <xsl:variable name="cvrgCondAll" select='cvrgCondAll'/>
            <xsl:variable name="cvrgCondBothTrueFalse" select='cvrgCondBothTrueFalse'/>
            
            <tr style="font-size: smaller">
                <td><xsl:value-of select="substring-after($qFuncName, ',,')"/></td>
                <td><xsl:value-of select="substring-before($qFuncName, '#')"/></td>
                <td><xsl:value-of select="substring-after(substring-before($qFuncName, ',,'), '#')"/></td>

                <xsl:call-template name="singleColorBarGraph">
                    <xsl:with-param name="color" select="$_neutralBarBkgColor"/>
                    <xsl:with-param name="nominator" select="$passed + $failed + $error"/>
                    <xsl:with-param name="denominator" select="$maxTestCases"/>
                    <xsl:with-param name="text" select="$passed + $failed + $error"/>
                </xsl:call-template>

                <xsl:call-template name="threeColorBarGraph">
                    <xsl:with-param name="leftNum" select="$passed"/>
                    <xsl:with-param name="middleNum" select="$failed"/>
                    <xsl:with-param name="rightNum" select="$error"/>
                </xsl:call-template>
                
                <xsl:choose>
                    <!-- show coverage graph only if available and coverage of group is measured -->
                    <xsl:when test="cvrgBytesAll or ../../coverageTestedOnly or ../../coverageAll">
                        <xsl:call-template name="singleColorBarGraph">
                            <xsl:with-param name="color" select="$_okBkgColor"/>
                            <xsl:with-param name="nominator" select="cvrgBytesExecuted"/>
                            <xsl:with-param name="denominator" select="cvrgBytesAll"/>
                            <xsl:with-param name="rightColor" select="$_errorBkgColor"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <td>/</td>
                    </xsl:otherwise>
                </xsl:choose>

                <xsl:choose>
                    <!-- show coverage graph only if available and coverage of group is measured -->
                    <xsl:when test="cvrgCondAll or ../../coverageTestedOnly or ../../coverageAll">
                        <xsl:call-template name="singleColorBarGraph">
                            <xsl:with-param name="color" select="$_okBkgColor"/>
                            <xsl:with-param name="nominator" select="cvrgCondFalse + cvrgCondTrue + cvrgCondBoth * 2"/>
                            <xsl:with-param name="denominator" select="cvrgCondAll * 2"/>
                            <xsl:with-param name="text">
                                <xsl:call-template name="percentageAsStr">
                                    <xsl:with-param name="nominator" select="cvrgCondFalse + cvrgCondTrue + cvrgCondBoth * 2"/>
                                    <xsl:with-param name="denominator" select="cvrgCondAll * 2"/>
                                </xsl:call-template>
                                &#160;(<xsl:value-of select='cvrgCondFalse'/>f, 
                                <xsl:value-of select='cvrgCondTrue'/>t, 
                                <xsl:value-of select='cvrgCondBoth'/>b) /
                                <xsl:value-of select='cvrgCondAll * 2'/> 
                            </xsl:with-param>
                            <xsl:with-param name="rightColor" select="$_errorBkgColor"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <td>/</td>
                    </xsl:otherwise>
                </xsl:choose>

                <td><xsl:value-of select="cvrgExecutionCount"/></td>
            </tr>
        </xsl:for-each>
        
    </table>
        
    </td></tr>
        
</xsl:template>


<xsl:template name="percentageAsStr">
    <xsl:param name="nominator"/>
    <xsl:param name="denominator"/>

	<xsl:choose>
		<xsl:when test="$denominator = '0' or not($denominator)">
			<xsl:value-of select="'/'" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of
				select='format-number(number($nominator div $denominator), "0.0%")' />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<xsl:template name="singleColorBarGraph">
    <!-- Creates table with two columns and two rows. Top row contains text,
         the bottom row contains empty cells with width proportional to parameters. -->
    <xsl:param name="color" select="$_okBkgColor"/>
    <xsl:param name="nominator"/>
    <xsl:param name="denominator"/>
    <xsl:param name="text"/>
    <xsl:param name="boldPrefixText"/>
    <xsl:param name="rightColor"/> <!-- if not specified, default cell bkg color is used. -->
    <xsl:param name="barGraphWidth" select="$barGraphW"/>

    <!-- First check for division by 0 or absence of values in XML. -->
    <xsl:variable name="percentage">
        <xsl:choose>
            <xsl:when test="$denominator = '0' or not($denominator)">
                <xsl:value-of select="'/'"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select='format-number(number($nominator div $denominator), "0.0%")'/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:variable name="barWidth">
        <xsl:choose>
            <xsl:when test="$denominator = '0' or not($denominator)">
                <xsl:value-of select="'0'"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select='format-number(number($nominator div $denominator * $barGraphWidth), "0")'/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:variable name="emptyCellWidth">
        <xsl:choose>
            <xsl:when test="$denominator = '0' or not($denominator)">
                <xsl:value-of select="$barGraphWidth"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select='format-number(number($barGraphWidth * (1 - $nominator div $denominator)), "0")'/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <!-- Now create table with text in top row, background color in bottom row. -->
    <td>  
        <table style='border: 0; width: {$barGraphWidth}px;'>
            <tr><td colspan='2' style='border: 0'>
                <xsl:choose> <!-- if $text is not specified, print percentage and values -->
                    <xsl:when test="$text or $text=0">
                        <b><xsl:value-of select="$boldPrefixText"/></b>
                        <xsl:value-of select='$text'/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select='$percentage'/>&#160;(<xsl:value-of select='$nominator'/>/<xsl:value-of select='$denominator'/>)
                    </xsl:otherwise>
                </xsl:choose>
            </td></tr>
            <tr><td style="width: {$barWidth}; height: 6px; border 1; border-spacing: 0; padding: 0; background-color: {$color}"></td>
            <!-- if $rightColor is specified, use it. -->
            <xsl:choose>
                <xsl:when test="$rightColor">
                    <td style='width: {$emptyCellWidth}px; border 1; border-spacing: 0; padding: 0; background-color: {$rightColor}'/>
                </xsl:when>
                <xsl:otherwise>
                    <td style='width: {$emptyCellWidth}px; border 1; border-spacing: 0; padding: 0'/>
                </xsl:otherwise>
            </xsl:choose>
            </tr>
        </table>
    </td>
</xsl:template>


<xsl:template name="threeColorBarGraph">
    <!-- Creates table with three columns and two rows. Top row contains text,
         the bottom row contains 3 empty cells with width proportional to parameters. -->
    <xsl:param name="leftNum"/>
    <xsl:param name="middleNum"/>
    <xsl:param name="rightNum"/>
    <xsl:param name="leftColor" select="$_okBkgColor"/>
    <xsl:param name="middleColor" select="$_failBkgColor"/>
    <xsl:param name="rightColor" select="$_errorBkgColor"/>

    <xsl:variable name='sum' select='$leftNum + $middleNum + $rightNum'/>

    <xsl:choose>
        <xsl:when test='$sum = 0'>
            <td>/</td>  <!-- Leave empty cell if there is no data. -->
        </xsl:when>
        <xsl:otherwise>

            <!-- First check for division by 0 or absence of values in XML. -->
            <xsl:variable name="leftPercentage" select='format-number(number($leftNum div $sum), "0.0%")'/>
            <xsl:variable name="middlePercentage" select='format-number(number($middleNum div $sum), "0.0%")'/>
            <xsl:variable name="rightPercentage" select='format-number(number($rightNum div $sum), "0.0%")'/>

            <xsl:variable name="leftBarWidth" select='format-number(number($leftNum div $sum * $barGraphW), "0")'/>
            <xsl:variable name="middleBarWidth" select='format-number(number($middleNum div $sum * $barGraphW), "0")'/>
            <xsl:variable name="rightBarWidth" select='format-number(number($rightNum div $sum * $barGraphW), "0")'/>


            <!-- Now create table with text in top row, background color in bottom row. -->
            <td>  
                <table style='border: 0; width: {$barGraphW}px;'>
                    <tr>
                        <td colspan='3' style='border: 0'>
                            <font size='2'>
                                <xsl:value-of select="$leftPercentage"/>&#160;(<xsl:value-of select="$leftNum"/>) / <xsl:value-of select="$middlePercentage"/>&#160;(<xsl:value-of select="$middleNum"/>) / <xsl:value-of select="$rightPercentage"/>&#160;(<xsl:value-of select="$rightNum"/>)
                            </font>
                        </td>
                    </tr>
                    <tr>
                        <td style="width: {$leftBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$leftColor}">
                        </td>
                        <td style="width: {$middleBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$middleColor}">
                        </td>
                        <td style="width: {$rightBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$rightColor}">
                        </td>
                    </tr>
                </table>
            </td>
        </xsl:otherwise>
    </xsl:choose>
    
</xsl:template>


<xsl:template name="fourColorBarGraph">
    <!-- Creates table with four columns and two rows. Top row contains text,
         the bottom row contains 4 empty cells with width proportional to parameters.
         The last column is proportional to (sum - leftNum + middleNum + rightNum)
    -->
    <xsl:param name="leftNum"/>
    <xsl:param name="middleNum"/>
    <xsl:param name="rightNum"/>
    <xsl:param name="complete"/>  <!-- may be more than leftNum + middleNum + rightNum -->
    <xsl:param name="leftColor" select="$_okBkgColor"/>
    <xsl:param name="middleColor" select="$_failBkgColor"/>
    <xsl:param name="rightColor" select="$_errorBkgColor"/>
    <xsl:param name="remainderColor" select="'#e6f8ff'"/> <!-- orange: #ff9422 -->

    <xsl:variable name='sum' select='$leftNum + $middleNum + $rightNum'/>
    <xsl:variable name='extendedBarGraphW' select='$barGraphW + 50'/>

    <xsl:choose>
        <xsl:when test='$sum = 0'>
            <td>/</td>  <!-- Leave empty cell if there is no data. -->
        </xsl:when>
        <xsl:otherwise>

            <!-- First check for division by 0 or absence of values in XML. -->
            <xsl:variable name="leftPercentage" select='format-number(number($leftNum div $complete), "0%")'/>
            <xsl:variable name="middlePercentage" select='format-number(number($middleNum div $complete), "0%")'/>
            <xsl:variable name="rightPercentage" select='format-number(number($rightNum div $complete), "0%")'/>
            <xsl:variable name="remainderPercentage" select='format-number(number(($complete - $sum) div $complete), "0%")'/>

            <xsl:variable name="leftBarWidth" select='format-number(number($leftNum div $sum * $extendedBarGraphW), "0")'/>
            <xsl:variable name="middleBarWidth" select='format-number(number($middleNum div $sum * $extendedBarGraphW), "0")'/>
            <xsl:variable name="rightBarWidth" select='format-number(number($rightNum div $sum * $extendedBarGraphW), "0")'/>
            <xsl:variable name="remainderBarWidth" select='format-number(number(($complete - $sum) div $sum * $extendedBarGraphW), "0")'/>


            <!-- Now create table with text in top row, background color in bottom row. -->
            <td>  
                <table style='border: 0; width: {$extendedBarGraphW}px;'>
                    <tr>
                        <td colspan='4' style='border: 0'>
                            <font size='2'>
                                <xsl:value-of select="$leftPercentage"/>&#160;(<xsl:value-of select="$leftNum"/>), <xsl:value-of select="$middlePercentage"/>&#160;(<xsl:value-of select="$middleNum"/>), <xsl:value-of select="$rightPercentage"/>&#160;(<xsl:value-of select="$rightNum"/>),
                                <!-- xsl:if test="not($complete = $sum)" -->
                                     <xsl:value-of select="$remainderPercentage"/>&#160;(<xsl:value-of select="$complete - $sum"/>)
                                <!-- /xsl:if -->
                            </font>
                        </td>
                    </tr>
                    <tr>
                        <td style="width: {$leftBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$leftColor}">
                        </td>
                        <td style="width: {$middleBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$middleColor}">
                        </td>
                        <td style="width: {$rightBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$rightColor}">
                        </td>
                        <td style="width: {$remainderBarWidth}px; height: 6px; border 0; border-spacing: 0; padding: 0; background-color: {$remainderColor}">
                        </td>
                    </tr>
                </table>
            </td>
        </xsl:otherwise>
    </xsl:choose>
    
</xsl:template>

</xsl:stylesheet>
  
