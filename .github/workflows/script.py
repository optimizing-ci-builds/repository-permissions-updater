name: Hosting checker
'on':
  issues:
    types:
    - opened
    - edited
jobs:
  hosting:
    runs-on: ubuntu-latest
    if: contains(github.event.issue.labels.*.name, 'hosting-request')
    steps:
    - uses: actions/checkout@v2
      with:
        ref: master
    - uses: actions/setup-java@v2
      with:
        distribution: temurin
        java-version: '11'
        cache: maven
    - name: Build with Maven
      run: mvn -B package -Dspotbugs.skip
    - name: Run hosting checker
      run: 'java -cp target/repository-permissions-updater-1.0-SNAPSHOT-bin/repository-permissions-updater-1.0-SNAPSHOT.jar
        io.jenkins.infra.repository_permissions_updater.hosting.HostingChecker ${{
        github.event.issue.number }}

        '
      env:
        GITHUB_OAUTH: ${{ secrets.GITHUB_TOKEN }}
