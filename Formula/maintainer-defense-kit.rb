class MaintainerDefenseKit < Formula
  desc "Audit repository governance and GitHub Actions risk offline"
  homepage "https://github.com/thangldw/awesome-maintainer-defense"
  url "https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.0.1/maintainer-defense-kit.py"
  sha256 "2b33f63f27f99109ce48160c5f376b16d54d94c645f45b0f19f3d17894b270ea"
  license "MIT"

  depends_on "python@3.12"

  def install
    libexec.install "maintainer-defense-kit.py" => "maintainer-defense"
    chmod 0755, libexec/"maintainer-defense"
    bin.write_exec_script libexec/"maintainer-defense"
  end

  test do
    assert_match "auditor 1.0.1; kit 1.0.1", shell_output("#{bin}/maintainer-defense --version")
    assert_match "findings", shell_output("#{bin}/maintainer-defense audit #{testpath} --format summary")
  end
end
